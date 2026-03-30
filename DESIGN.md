# Voice Chat Bridge - 设计草案

## 目标
把多渠道语音消息统一桥接成：

语音输入 -> 本地/远程转写 -> LLM 对话 -> 可选 TTS 回传

## 当前已完成
- 本地 vosk 中文小模型可用
- `transcribe_audio.py` 可处理 `.ogg/opus` 音频
- 飞书语音样本已验证可转写

## v1 最小可用版
### 输入
- 手动提供音频文件路径

### 处理
- ffmpeg 转 16k 单声道 wav
- vosk 本地模型转写

### 输出
- 标准输出文本

## v1.1
- 接飞书语音消息路径
- 自动触发转写
- 输出文字答复

## v1.2
- 接 TTS 工具
- 自动语音回复
- 增加开关：只回文字 / 只回语音 / 双回
- 配置集中化（pydantic + dotenv），提取通用校验与依赖检查（utils）
- 接 TTS 工具
- 自动语音回复
- 增加开关：只回文字 / 只回语音 / 双回

## 渠道支持现状
- Feishu：已完成闭环（下载/转写/回复/TTS/OGG 输出）
- Telegram：新增支持（Bot API 下载 voice -> STT -> 模板回复 -> TTS -> sendVoice 回传）
- Discord：规划中
- WeChat / openclaw-weixin：规划中

## 当前依赖
- ffmpeg
- Python 环境（默认取当前解释器，可由 `VOSK_PYTHON` 覆盖）
- `edge-tts` 可执行文件（默认从 PATH 查找，可由 `EDGE_TTS_BIN` 覆盖）
- `/tmp/vosk-model/vosk-model-small-cn-0.22`（可由 `VOSK_MODEL_DIR` 或 `--model-dir` 覆盖）

## 注意
- 当前中文识别精度够用但一般
- 后续可换更大模型或做热词纠错
