#!/usr/bin/env python3
"""
音频转写模块：使用 Vosk 模型将音频文件转写为文本。
支持格式：OGG/Opus, WAV, MP3 等 (需 ffmpeg 支持)
模型：Vosk 中文小模型 (vosk-model-small-cn-0.22)
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from utils import ensure_file

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 配置
TEMP_DIR = os.path.join("/tmp", "voice-chat")
os.makedirs(TEMP_DIR, exist_ok=True)

from config import get_settings
_settings = get_settings()
VENV_PY = _settings.VOSK_PYTHON
MODEL_DIR = _settings.VOSK_MODEL_DIR
TEMP_WAV_PREFIX = 'vosk_transcribe_'
TEMP_WAV_SUFFIX = '.wav'


class TranscriptionError(Exception):
    """转写过程中的自定义异常"""
    pass


def transcribe(src_audio: str, model_dir: Optional[str] = None) -> str:
    """
    将音频文件转写为文本。

    Args:
        src_audio: 输入音频文件路径 (支持 ogg, opus, wav, mp3 等)
        model_dir: Vosk 模型目录路径，默认为配置常量

    Returns:
        转写后的文本内容

    Raises:
        FileNotFoundError: 音频文件不存在
        RuntimeError: 模型未找到或转写失败
        subprocess.CalledProcessError: ffmpeg 转换失败

    Example:
        >>> text = transcribe('/tmp/audio.ogg')
        >>> print(text)
        '你好，这是一个测试'
    """
    src_audio = ensure_file(src_audio)

    model_dir = model_dir or MODEL_DIR
    if not os.path.isdir(model_dir):
        raise RuntimeError(f"Vosk 模型目录不存在：{model_dir}")

    if shutil.which('ffmpeg') is None:
        raise TranscriptionError("ffmpeg 未安装或不在 PATH 中")

    logger.info(f"开始转写音频：{src_audio}")
    logger.info(f"使用模型目录：{model_dir}")

    # 创建临时 WAV 文件
    with tempfile.NamedTemporaryFile(
        suffix=TEMP_WAV_SUFFIX,
        prefix=TEMP_WAV_PREFIX,
        dir=TEMP_DIR,
        delete=False
    ) as tmp_wav:
        wav_path = tmp_wav.name

    try:
        # 使用 ffmpeg 转换为 16kHz 单声道 WAV (Vosk 要求格式)
        logger.info("正在转换音频格式...")
        ffmpeg_cmd = [
            'ffmpeg', '-y',
            '-i', str(src_audio),
            '-ar', '16000',
            '-ac', '1',
            '-f', 'wav',
            wav_path
        ]
        result = subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            timeout=60
        )

        if not os.path.exists(wav_path) or os.path.getsize(wav_path) == 0:
            raise TranscriptionError("ffmpeg 转换生成的 WAV 文件为空")

        logger.info("音频格式转换完成，开始 Vosk 转写...")

        # 执行 Vosk 转写
        code = f'''
import json
import wave
from vosk import Model, KaldiRecognizer

wav_path = {repr(wav_path)}
model_dir = {repr(model_dir)}

wf = wave.open(wav_path, 'rb')
model = Model(model_dir)
rec = KaldiRecognizer(model, wf.getframerate())

texts = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = json.loads(rec.Result())
        text = result.get('text', '')
        if text:
            texts.append(text)

# 处理最终结果
final_result = json.loads(rec.FinalResult())
final_text = final_result.get('text', '')
if final_text:
    texts.append(final_text)

print(' '.join(texts).strip())
'''
        output = subprocess.check_output(
            [VENV_PY, '-c', code],
            text=True,
            timeout=120,
            stderr=subprocess.PIPE
        )
        result_text = output.strip()
        logger.info(f"转写完成：{result_text}")
        return result_text

    except subprocess.TimeoutExpired:
        logger.error("转写过程超时")
        raise TranscriptionError("转写过程超时")
    except subprocess.CalledProcessError as e:
        # Python 3.13+ 中 stderr 已经是 str，不需要 decode
        stderr_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='ignore') if e.stderr else '未知错误'
        logger.error(f"转写失败：{stderr_msg}")
        raise TranscriptionError(f"转写失败：{stderr_msg}")
    finally:
        # 清理临时 WAV 文件
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
                logger.debug(f"已清理临时文件：{wav_path}")
            except OSError as e:
                logger.warning(f"无法删除临时文件 {wav_path}: {e}")


def main():
    """命令行入口点"""
    parser = argparse.ArgumentParser(description='将音频文件转写为文本')
    parser.add_argument('audio_file', help='输入音频文件路径')
    parser.add_argument(
        '--model-dir',
        default=None,
        help='Vosk 模型目录（默认读取 VOSK_MODEL_DIR 或内置默认值）'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细日志'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        transcript = transcribe(args.audio_file, model_dir=args.model_dir)
        if transcript:
            print(transcript)
            sys.exit(0)
        else:
            logger.error("转写结果为空")
            print('ERROR: 转写结果为空', file=sys.stderr)
            sys.exit(2)
    except FileNotFoundError as e:
        logger.error(f"文件未找到：{e}")
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(1)
    except TranscriptionError as e:
        logger.error(f"转写错误：{e}")
        print(f'ERROR: {e}', file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        logger.exception(f"未预期的错误：{e}")
        print(f'ERROR: 未预期的错误 - {e}', file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
