"""
Quick verification script to ensure all components are working.
Run this before submitting to judges.
"""

import sys
import importlib.util


def check_python_version():
    """Verify Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (requires 3.8+)")
        return False


def check_dependencies():
    """Verify all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required = [
        "fastapi",
        "uvicorn",
        "edge_tts",
        "transformers",
        "torch",
        "pydantic",
        "aiofiles"
    ]
    
    all_installed = True
    for package in required:
        spec = importlib.util.find_spec(package.replace("-", "_"))
        if spec is not None:
            print(f"   ✅ {package}")
        else:
            print(f"   ❌ {package} (not installed)")
            all_installed = False
    
    return all_installed


def check_file_structure():
    """Verify all required files exist"""
    print("\n🔍 Checking file structure...")
    
    import os
    
    required_files = [
        "main.py",
        "emotion_detector.py",
        "tts_engine.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "static/index.html"
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
            all_exist = False
    
    return all_exist


def check_imports():
    """Verify custom modules can be imported"""
    print("\n🔍 Checking custom modules...")
    
    modules = [
        ("config", "config.py"),
        ("emotion_detector", "emotion_detector.py"),
        ("tts_engine", "tts_engine.py")
    ]
    
    all_importable = True
    for module_name, file_name in modules:
        try:
            importlib.import_module(module_name)
            print(f"   ✅ {file_name}")
        except Exception as e:
            print(f"   ❌ {file_name} ({str(e)[:50]}...)")
            all_importable = False
    
    return all_importable


def test_emotion_detection():
    """Quick test of emotion detection"""
    print("\n🔍 Testing emotion detection...")
    
    try:
        from emotion_detector import EmotionDetector
        
        print("   ⏳ Loading model (this may take a moment)...")
        detector = EmotionDetector()
        
        test_text = "This is absolutely amazing!"
        emotion, confidence, _ = detector.detect_emotion(test_text)
        
        print(f"   ✅ Test: '{test_text}'")
        print(f"      → Emotion: {emotion} (confidence: {confidence:.2%})")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False


def test_config():
    """Verify emotion mapping configuration"""
    print("\n🔍 Testing emotion-to-voice mapping...")
    
    try:
        import config
        
        emotions = list(config.EMOTION_VOICE_MAP.keys())
        print(f"   ✅ Found {len(emotions)} emotions: {', '.join(emotions)}")
        
        # Test parameter retrieval
        params = config.get_voice_parameters("joy", 0.8)
        print(f"   ✅ Joy parameters: rate={params['rate']}, pitch={params['pitch']}, volume={params['volume']}")
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🎭 THE EMPATHY ENGINE - VERIFICATION SCRIPT")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Module Imports", check_imports),
        ("Configuration", test_config),
        ("Emotion Detection", test_emotion_detection)
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready for submission!")
        print("\nNext steps:")
        print("1. Run: python main.py")
        print("2. Open: http://localhost:8000")
        print("3. Test with sample texts")
    else:
        print("❌ SOME CHECKS FAILED - Please fix issues above")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Ensure all files are in the correct location")
        print("- Check internet connection (required for first run)")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
