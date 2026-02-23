# The Empathy Engine: Giving AI a Human Voice

The Empathy Engine is a service that dynamically modulates the vocal characteristics of synthesized speech based on the detected emotion of source text. It bridges the gap between text-based sentiment and expressive, human-like audio output.

## Features

- **Emotion Detection**: Uses a fine-tuned DistilRoBERTa model to classify text into 7 emotional categories (Joy, Anger, Sadness, Fear, Surprise, Disgust, Neutral).
- **Dynamic Modulation**: Programmatically alters vocal **Rate**, **Pitch**, and **Volume** based on the detected emotion.
- **Expressive TTS**: Leverages `edge-tts` for high-quality, neural voice synthesis.
- **Premium Web Interface**: A sleek, dark-themed UI for instant text input and audio playback.

## Tech Stack

- **Backend**: Python, FastAPI, Transformers (PyTorch), Edge-TTS.
- **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript.

## Setup and Startup Instructions

### 1. Local Setup
1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd Empathy.Engine
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python main.py
   ```
4. **Access the Interface**:
   Open [http://localhost:8000](http://localhost:8000) in your browser.

### 2. Deployment (Render)
To deploy using the provided `render.yaml`:
1. Push your code to a GitHub repository.
2. Log in to **Render** and create a new **Blueprint**.
3. Select your repository and click **Apply**.
4. The service will build and deploy automatically.

## Emotion-to-Voice Mapping Logic

The engine uses the following mapping strategy to achieve emotional resonance:

| Emotion  | Rate    | Pitch   | Volume  | Rationale |
|----------|---------|---------|---------|-----------|
| **Joy**  | +25%    | +15Hz   | +10%    | Happy speech is typically faster and higher-pitched. |
| **Anger**| +10%    | -5Hz    | +30%    | Angry speech is loud and often has a lower, harsher tone. |
| **Sadness**| -20%  | -10Hz   | -20%    | Sad speech is slower, lower-pitched, and quieter. |
| **Fear** | +30%    | +20Hz   | -10%    | Fearful speech is rapid and high-pitched but lacks volume. |
| **Surprise**| +40% | +25Hz   | +15%    | Surprise is fast and high-pitched. |
| **Neutral**| +0%   | +0Hz    | +0%     | Standard monotonic delivery. |

## Design Choices

- **Model Choice**: `j-hartmann/emotion-english-distilroberta-base` was chosen for its high accuracy and ability to distinguish between 7 distinct emotions, allowing for more granular modulation than a simple positive/negative model.
- **TTS Engine**: `edge-tts` (Microsoft Edge TTS API) provides significantly better prosody and naturalness compared to offline alternatives like `pyttsx3`, making the "empathy" effect much more convincing.
- **UI Design**: The interface uses a dark theme with backdrop filters (glassmorphism) to provide a premium, futuristic feel consistent with the "Empathy Engine" concept.
