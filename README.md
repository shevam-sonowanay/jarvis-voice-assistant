# JARVIS - Multilingual Desktop AI Assistant

A voice-controlled desktop AI assistant powered by Google Gemini, featuring real-time multilingual support (**English, Hindi, and Marathi**), barge-in interruption, and automated Windows system controls.

## Features
- **Multilingual Voice & TTS:** Understands and responds naturally in English, Hindi, and Marathi using `edge-tts`.
- **Desktop Automation:** Opens local applications (Scilab, Chrome, Notepad, etc.), takes screenshots, and controls system volume.
- **Media & Browser Control:** Plays songs/videos directly on Spotify and YouTube and handles screen scrolling and playback.
- **WhatsApp Integration:** Sends WhatsApp messages directly to saved contacts via the desktop app.
- **Wikipedia Knowledge:** Fetches quick factual summaries on demand.

## Tech Stack
- **Language:** Python
- **AI & Tool Calling:** Google Gemini (`google-genai` SDK)
- **Speech & Audio:** `SpeechRecognition`, `PyAudio`, `edge-tts`, `pygame`
- **Automation:** `pyautogui`, `pywhatkit`, `wikipedia`, `python-dotenv`

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd jarvis-voice-assistant/Python/JARVIS
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project folder and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
4. Run JARVIS:
   ```bash
   python jarvis.py
   ```
