#!/usr/bin/env python3
"""
Centralized configuration for Voice Chat Bridge.
Uses pydantic BaseSettings and python-dotenv to load environment variables.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    # STT Engine Selection
    STT_ENGINE: str = "sensevoice"  # Options: "sensevoice", "vosk", "auto"

    # SenseVoice Configuration
    SENSEVOICE_MODEL_DIR: str = "/tmp/sensevoice-model"
    SENSEVOICE_MODEL_NAME: str = "iic/SenseVoiceSmall"

    # Vosk Configuration (fallback)
    VOSK_PYTHON: str = sys.executable
    VOSK_MODEL_DIR: str = "/tmp/vosk-model/vosk-model-small-cn-0.22"

    # Text-to-speech (edge-tts)
    EDGE_TTS_BIN: Optional[str] = None
    DEFAULT_VOICE: str = "zh-CN-YunxiNeural"

    # LLM Configuration (optional, for future use)
    llm_base_url: Optional[str] = None
    llm_api_key: Optional[str] = None
    llm_model: Optional[str] = None

    # Note: All chat platform credentials (Telegram/Feishu/etc.) have been removed.
    # This project is now a pure processing skill to be orchestrated by OpenClaw.

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    # Load .env if present; environment variables still take precedence
    load_dotenv(override=False)
    return Settings()
