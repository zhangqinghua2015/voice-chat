# Voice Chat Bridge - 设计文档

## 目标
把多渠道语音消息统一桥接成：
**语音输入 → 本地/远程转写 → LLM 对话 → 可选 TTS 回传**

## 当前已完成
- ✅ SenseVoice（首选）+ Vosk（备份）双引擎 STT
- ✅ 自动 fallback 机制：SenseVoice 失败时自动切换 Vosk
- ✅ 中英文混合识别优化
- ✅ `transcribe_audio.py` 可处理 `.ogg/opus` 音频
- ✅ 飞书语音样本已验证可转写
- ✅ 支持 Telegram 语音下载与回传
- ✅ Edge TTS 失败自动降级到 `pyttsx3`

## 版本历程

### v1.0 - 最小可用版
- **输入**：手动提供音频文件路径
- **处理**：ffmpeg 转 16k 单声道 wav → vosk 本地模型转写
- **输出**：标准输出文本

### v1.1 - 飞书集成
- 接入飞书语音消息路径
- 自动触发转写
- 输出文字答复

### v1.2 - 完整闭环
- 接入 TTS 工具
- 自动语音回复
- 增加开关：只回文字 / 只回语音 / 双回
- 配置集中化（pydantic + dotenv）
- 提取通用校验与依赖检查（utils）

### v2.0 - 双引擎升级
- **新增**：SenseVoice 引擎（首选，中英文混合识别）
- **新增**：自动 fallback 机制（SenseVoice 失败时切换 Vosk）
- **新增**：引擎策略配置（sensevoice/vosk/auto）
- **优化**：中英文混合识别准确率
- **兼容**：保持 Vosk 作为备份方案

## 渠道支持现状
| 渠道 | 状态 | 说明 |
|------|------|------|
| Feishu | ✅ 已完成 | 下载/转写/回复/TTS/OGG 输出闭环 |
| Telegram | ✅ 已完成 | Bot API 下载 voice → STT → 模板回复 → TTS → sendVoice 回传 |
| Discord | 🚧 规划中 | |
| WeChat / openclaw-weixin | 🚧 规划中 | |

## STT 引擎对比

### SenseVoice（首选）
- **优势**：
  - 原生支持中英文混合识别
  - 识别准确率优于 Vosk
  - 推理速度快（70ms 处理 10 秒音频）
  - 支持多语言（50+ 语言）
- **劣势**：
  - 依赖 `funasr-onnx`（需额外安装）
  - 模型文件较大（~100MB）
  - 首次加载较慢

### Vosk（备份）
- **优势**：
  - 轻量级，模型文件小（~40MB）
  - 纯 Python 实现，部署简单
  - 离线运行，无网络依赖
- **劣势**：
  - 中英文混合识别效果一般
  - 需要语言切换
  - 准确率低于 SenseVoice

### Fallback 策略
```python
# 策略 1: 仅使用 SenseVoice
transcribe(audio, engine="sensevoice")

# 策略 2: 仅使用 Vosk
transcribe(audio, engine="vosk")

# 策略 3: 自动 fallback（推荐）
transcribe(audio, engine="auto")  # SenseVoice 失败时自动切换 Vosk
```

## 当前依赖
- `ffmpeg`：音频格式转换
- `funasr-onnx`：SenseVoice 引擎（首选）
- `vosk`：Vosk 引擎（备份）
- Python 环境（默认取当前解释器，可由 `VOSK_PYTHON` 覆盖）
- `edge-tts` 可执行文件（默认从 PATH 查找，可由 `EDGE_TTS_BIN` 覆盖）
- `/tmp/sensevoice-model`（SenseVoice 模型目录，可由 `SENSEVOICE_MODEL_DIR` 覆盖）
- `/tmp/vosk-model/vosk-model-small-cn-0.22`（Vosk 模型目录，可由 `VOSK_MODEL_DIR` 覆盖）

## 配置说明

### 环境变量
| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `STT_ENGINE` | `sensevoice` | STT 引擎策略（sensevoice/vosk/auto） |
| `SENSEVOICE_MODEL_DIR` | `/tmp/sensevoice-model` | SenseVoice 模型目录 |
| `SENSEVOICE_MODEL_NAME` | `iic/SenseVoiceSmall` | SenseVoice 模型名称 |
| `VOSK_PYTHON` | `sys.executable` | Vosk 使用的 Python 解释器 |
| `VOSK_MODEL_DIR` | `/tmp/vosk-model/vosk-model-small-cn-0.22` | Vosk 模型目录 |
| `EDGE_TTS_BIN` | `edge-tts` | Edge TTS 可执行文件路径 |
| `DEFAULT_VOICE` | `zh-CN-YunxiNeural` | TTS 默认音色 |

## 注意事项
- SenseVoice 模型会在首次运行时自动下载到 `~/.cache/modelscope/`
- Vosk 模型需要手动下载（参考 README.md）
- 所有处理必须在**当前会话**中执行，**严禁新开子会话**
- termux 环境下，SenseVoice 使用 CPU 推理（无 GPU 加速）
