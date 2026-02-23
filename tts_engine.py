import edge_tts
import asyncio
import os
import logging
from datetime import datetime
import config

logger = logging.getLogger(__name__)

class EmotionalTTSEngine:
    def __init__(self, voice: str = config.DEFAULT_VOICE):
        self.voice = voice

    async def synthesize_with_emotion(self, text: str, emotion: str, confidence: float = 1.0, output_filename: Optional[str] = None) -> str:
        # Handles speech synthesis with emotional modulation
        params = config.get_voice_parameters(emotion, confidence)
        if not output_filename:
            output_filename = f"output_{emotion}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        path = os.path.join(config.OUTPUT_DIR, output_filename)
        try:
            comm = edge_tts.Communicate(text=text, voice=self.voice, rate=params['rate'], pitch=params['pitch'], volume=params['volume'])
            await comm.save(path)
            return path
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            raise

class EmpathyEngine:
    def __init__(self, emotion_detector, tts_engine: EmotionalTTSEngine):
        self.emotion_detector = emotion_detector
        self.tts_engine = tts_engine

    async def process_text(self, text: str, output_filename: Optional[str] = None) -> dict:
        emotion, conf, scores = self.emotion_detector.detect_emotion(text)
        path = await self.tts_engine.synthesize_with_emotion(text, emotion, conf, output_filename)
        return {
            "text": text,
            "emotion": {
                "label": emotion, "confidence": round(conf, 4),
                "description": config.EMOTION_VOICE_MAP.get(emotion, config.EMOTION_VOICE_MAP["neutral"])["description"],
                "all_scores": [{"emotion": s["label"], "score": round(s["score"], 4)} for s in scores[:3]]
            },
            "voice_modulation": config.get_voice_parameters(emotion, conf),
            "audio_file": os.path.basename(path), "audio_path": path
        }
