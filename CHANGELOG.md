# Changelog

All notable changes to this project will be documented in this file.

## v1.3 (2026-03-29)
- Telegram channel support:
  - New scripts: `scripts/telegram_voice_handler.py`, `scripts/run_telegram_voice_chat.py`
  - Added Telegram config to `scripts/config.py`: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`
  - Added `requests` to requirements
  - Added tests: `tests/test_telegram_voice_handler.py`
  - Updated README/SKILL/DESIGN with Telegram usage and design

## v1.2 (2026-03-29)
- Config centralized via pydantic BaseSettings (`scripts/config.py`)
- Extracted shared utilities (`scripts/utils.py`): file checks, ffmpeg/edge-tts resolution
- Added logging to TTS and Feishu handler; standardized CLI behavior
- `run_feishu_voice_chat.py` now reads reply text from env `VOICE_CHAT_REPLY_TEXT`
- README updated with architecture diagram, configuration, and entry usage
- SKILL.md/DESIGN.md refined; added this CHANGELOG

## v1.1 (2026-03-29)
- Feishu voice message full loop
- Documentation and type hints
- Error handling and logging improvements
- Added requirements.txt and .gitignore

## v1.0 (2026-03-29)
- Initial release: STT (Vosk), TTS (edge-tts), Feishu format compatibility
