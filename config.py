import os
from typing import Dict, Any

OUTPUT_DIR = "output"
STATIC_DIR = "static"
EMOTION_MODEL = "j-hartmann/emotion-english-distilroberta-base"

DEFAULT_VOICE = "en-US-AriaNeural"
DEFAULT_RATE = "+0%"
DEFAULT_PITCH = "+0Hz"
DEFAULT_VOLUME = "+0%"

EMOTION_VOICE_MAP: Dict[str, Dict[str, str]] = {
    "joy": {"rate": "+15%", "pitch": "+50Hz", "volume": "+10%", "description": "Enthusiastic and upbeat"},
    "anger": {"rate": "+10%", "pitch": "+20Hz", "volume": "+20%", "description": "Intense and assertive"},
    "sadness": {"rate": "-20%", "pitch": "-50Hz", "volume": "-10%", "description": "Gentle and somber"},
    "fear": {"rate": "+20%", "pitch": "+80Hz", "volume": "-5%", "description": "Anxious and hurried"},
    "surprise": {"rate": "+10%", "pitch": "+60Hz", "volume": "+15%", "description": "Excited and astonished"},
    "disgust": {"rate": "-10%", "pitch": "-30Hz", "volume": "+5%", "description": "Disapproving and measured"},
    "neutral": {"rate": "+0%", "pitch": "+0Hz", "volume": "+0%", "description": "Calm and professional"}
}

def get_voice_parameters(emotion: str, intensity: float = 1.0) -> Dict[str, Any]:
    # Scale voice parameters based on emotion and intensity
    params = EMOTION_VOICE_MAP.get(emotion, EMOTION_VOICE_MAP["neutral"]).copy()
    if intensity < 1.0:
        for param in ["rate", "pitch", "volume"]:
            value = params[param]
            if value != "+0%" and value != "+0Hz":
                numeric = int(value[1:-1]) if value[-1] == '%' else int(value[1:-2])
                params[param] = f"{value[0]}{int(numeric * intensity)}{value[-1] if value[-1] == '%' else value[-2:]}"
    return params

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)
