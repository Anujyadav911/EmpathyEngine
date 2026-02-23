"""
FastAPI Backend for Empathy Engine.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
import logging
import os
import uvicorn

from emotion_detector import get_emotion_detector
from tts_engine import EmotionalTTSEngine, EmpathyEngine
import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    global empathy_engine
    try:
        emotion_detector = get_emotion_detector()
        tts_engine = EmotionalTTSEngine()
        empathy_engine = EmpathyEngine(emotion_detector, tts_engine)
        logger.info("Empathy Engine ready")
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        raise
    yield

app = FastAPI(title="Empathy Engine", version="1.0.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=config.STATIC_DIR), name="static")

class SynthesisRequest(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"text": "This is amazing!", "voice": "en-US-AriaNeural"}})
    text: str = Field(..., min_length=1, max_length=5000)
    voice: Optional[str] = Field(default=config.DEFAULT_VOICE)

class EmotionScore(BaseModel):
    emotion: str
    score: float

class EmotionInfo(BaseModel):
    label: str
    confidence: float
    description: str
    all_scores: List[EmotionScore]

class VoiceModulation(BaseModel):
    rate: str
    pitch: str
    volume: str

class SynthesisResponse(BaseModel):
    text: str
    emotion: EmotionInfo
    voice_modulation: VoiceModulation
    audio_file: str
    download_url: str

empathy_engine: Optional[EmpathyEngine] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(config.STATIC_DIR, "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return HTMLResponse(content="<h1>Empathy Engine</h1>", status_code=200)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "engine_ready": empathy_engine is not None}

@app.post("/synthesize", response_model=SynthesisResponse)
async def synthesize_speech(request: SynthesisRequest):
    if empathy_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    try:
        result = await empathy_engine.process_text(request.text)
        return SynthesisResponse(
            text=result["text"],
            emotion=EmotionInfo(**result["emotion"]),
            voice_modulation=VoiceModulation(**result["voice_modulation"]),
            audio_file=result["audio_file"],
            download_url=f"/audio/{result['audio_file']}"
        )
    except Exception as e:
        logger.error(f"Synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/audio/{filename}")
async def get_audio_file(filename: str):
    file_path = os.path.join(config.OUTPUT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=file_path, media_type="audio/wav", filename=filename)

@app.get("/emotions")
async def list_emotions():
    return {
        "emotions": [
            {
                "emotion": e,
                "description": p["description"],
                "modulation": {"rate": p["rate"], "pitch": p["pitch"], "volume": p["volume"]}
            }
            for e, p in config.EMOTION_VOICE_MAP.items()
        ]
    }

@app.post("/analyze")
async def analyze_emotion(request: SynthesisRequest):
    if empathy_engine is None:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    return empathy_engine.emotion_detector.get_detailed_analysis(request.text)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
