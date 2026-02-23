import argparse
import asyncio
import sys
from emotion_detector import get_emotion_detector
from tts_engine import EmotionalTTSEngine, EmpathyEngine
import config

async def interactive(engine):
    # Main loop for terminal interaction
    while True:
        try:
            t = input("Text: ").strip()
            if not t: continue
            if t.lower() in ['q', 'quit']: break
            res = await engine.process_text(t)
            print(f"Emotion: {res['emotion']['label']} ({res['emotion']['confidence']:.1%})")
            print(f"Audio: {res['audio_path']}")
        except KeyboardInterrupt: break

async def main():
    p = argparse.ArgumentParser()
    p.add_argument('-t', '--text')
    p.add_argument('-i', '--interactive', action='store_true')
    args = p.parse_args()

    engine = EmpathyEngine(get_emotion_detector(), EmotionalTTSEngine())
    if args.interactive: await interactive(engine)
    elif args.text:
        res = await engine.process_text(args.text)
        print(f"Result: {res['audio_path']}")

if __name__ == "__main__":
    asyncio.run(main())
