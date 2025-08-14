"""
EchoVerse Configuration File
Contains all API keys, model configurations, and system settings
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face Configuration
HF_API_KEY = "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"
HF_API_BASE = "https://api-inference.huggingface.co/models"

# Model Configurations
TEXT_TO_TEXT_MODEL = "ibm-granite/granite-3.0-2b-instruct"
TEXT_TO_SPEECH_MODEL = "microsoft/speecht5_tts"
# Alternative TTS models that work better with HF API
TTS_MODELS = {
    "espnet": "espnet/kan-bayashi_ljspeech_vits",
    "facebook": "facebook/mms-tts-eng",
    "microsoft": "microsoft/speecht5_tts",
    "suno": "suno/bark-small"
}

# Voice Options
VOICE_OPTIONS = {
    "Lisa": "lisa",
    "Michael": "michael", 
    "Allison": "allison",
    "Emma": "emma",
    "Brian": "brian"
}

# Tone Options
TONE_OPTIONS = {
    "Neutral": {
        "description": "Clear, balanced narration",
        "prompt_modifier": "Rewrite this text in a neutral, clear, and balanced tone while maintaining all original information and meaning."
    },
    "Suspenseful": {
        "description": "Dramatic, tension-building style",
        "prompt_modifier": "Rewrite this text in a suspenseful, dramatic tone that builds tension and intrigue while preserving all original information."
    },
    "Inspiring": {
        "description": "Motivational, uplifting delivery",
        "prompt_modifier": "Rewrite this text in an inspiring, motivational tone that uplifts and energizes while keeping all original information intact."
    },
    "Educational": {
        "description": "Clear, instructional style",
        "prompt_modifier": "Rewrite this text in an educational, instructional tone that is clear and easy to understand while maintaining all original content."
    },
    "Storytelling": {
        "description": "Narrative, engaging style",
        "prompt_modifier": "Rewrite this text in a storytelling tone that is engaging and narrative while preserving all original information."
    }
}

# Intensity Levels
INTENSITY_LEVELS = {
    "Low": "subtle and gentle",
    "Medium": "moderate and balanced", 
    "High": "strong and pronounced"
}

# Language Options
LANGUAGE_OPTIONS = {
    "English": "en",
    "Spanish": "es",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Chinese": "zh",
    "Japanese": "ja",
    "Korean": "ko"
}

# App Configuration
APP_TITLE = "EchoVerse - AI Audiobook Creator"
APP_ICON = "🎧"
PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# File Upload Settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_FILE_TYPES = ["txt", "pdf"]

# Audio Settings
AUDIO_SAMPLE_RATE = 22050
AUDIO_FORMAT = "mp3"
MAX_TEXT_LENGTH = 50000  # characters

# Session State Keys
SESSION_KEYS = {
    "authenticated": "authenticated",
    "username": "username",
    "current_page": "current_page",
    "original_text": "original_text",
    "rewritten_text": "rewritten_text",
    "audio_data": "audio_data",
    "bookmarks": "bookmarks",
    "notes": "notes"
}
