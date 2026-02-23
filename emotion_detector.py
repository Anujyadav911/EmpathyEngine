from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class EmotionDetector:
    def __init__(self, model: str = "j-hartmann/emotion-english-distilroberta-base"):
        # Loads the transformer model for emotion classification
        try:
            self.classifier = pipeline("text-classification", model=model, top_k=None)
        except Exception as e:
            logger.error(f"Model Load Error: {e}")
            raise
    
    def detect_emotion(self, text: str):
        if not text or not text.strip():
            return "neutral", 1.0, [{"label": "neutral", "score": 1.0}]
        preds = self.classifier(text[:512])[0]
        sorted_preds = sorted(preds, key=lambda x: x['score'], reverse=True)
        return sorted_preds[0]['label'], sorted_preds[0]['score'], sorted_preds
    
    def get_detailed_analysis(self, text: str):
        label, conf, scores = self.detect_emotion(text)
        return {
            "text": text, "dominant_emotion": label, "confidence": round(conf, 4),
            "all_emotions": [{"emotion": s["label"], "confidence": round(s["score"], 4)} for s in scores]
        }

_inst = None
def get_emotion_detector():
    global _inst
    if _inst is None: _inst = EmotionDetector()
    return _inst
