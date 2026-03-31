# Changelog

All notable changes to this project will be documented in this file.

## v1.4 (2026-03-31)
- **文档优化**：
  - 更新 `README.md`：在语音处理流程第 1 点添加"**重点注意**"，强调**严禁新开子会话**。
  - 优化 `DESIGN.md`：精简重复内容，补充渠道支持表格，新增注意事项。
  - 更新本 `CHANGELOG.md`。
- **格式修正**：确保流程步骤之间有空行，提升可读性。

## v1.3 (2026-03-29)
- Telegram channel support:
  - New scripts: `scripts/telegram_voice_handler.py`, `scripts/run_telegram_voice_chat.py`
  - Added Telegram config to `scripts/config.py`: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
  - Added `requests` to requirements
  - Added tests: `tests/test_telegram_voice_handler.py`

## v1.2 (2026-03-28)
- 完整闭环：接入 TTS 工具，自动语音回复
- 增加开关：只回文字 / 只回语音 / 双回
- 配置集中化（pydantic + dotenv）
- 提取通用校验与依赖检查（utils）

## v1.1 (2026-03-27)
- 飞书集成：接入飞书语音消息路径
- 自动触发转写
- 输出文字答复

## v1.0 (2026-03-26)
- 最小可用版：手动提供音频文件路径
- ffmpeg 转 16k 单声道 wav → vosk 本地模型转写
- 输出标准文本
