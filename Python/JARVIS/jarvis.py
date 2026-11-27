import os
import time
import queue
import asyncio
import datetime
import threading
import webbrowser
import urllib.parse
import subprocess
import speech_recognition as sr
import pyautogui
import wikipedia
import edge_tts
import pygame
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types

# 1. Initialize Audio Player & Barge-In State
pygame.mixer.init()
command_queue = queue.Queue()
stop_speaking_event = threading.Event()
is_speaking = False

# 2. Save Your Frequent Contacts Here (Always include country code like +91)
CONTACTS = {
    "mom": "+910000000000",
    "dad": "+910000000000",
    "friend": "+910000000000",
}


# 3. Save Your Frequent Windows Apps Here
APPS = {
    "scilab": r"C:\Program Files\scilab-2027.0.0\bin\WScilex.exe",
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "chrome": "chrome.exe",
    "whatsapp": "whatsapp://",
    "spotify": "spotify:",
}

# 4. Non-Blocking, Interruptible Multilingual Text-to-Speech (Edge-TTS)
async def _generate_speech(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice, rate="+8%")
    await communicate.save(output_file)

def interrupt_jarvis():
    """Immediately stops JARVIS mid-sentence when you start talking."""
    global is_speaking
    if is_speaking or pygame.mixer.music.get_busy():
        stop_speaking_event.set()
        pygame.mixer.music.stop()
        is_speaking = False
        print("\n[Interrupted]")

def speak(text, lang_code="en"):
    """Speaks text in a background thread so you can interrupt anytime."""
    global is_speaking
    stop_speaking_event.clear()
    print(f"JARVIS: {text}")

    voice_map = {
        "en": "en-GB-RyanNeural",      # British JARVIS-style English
        "hi": "hi-IN-MadhurNeural",    # Hindi
        "mr": "mr-IN-ManoharNeural",   # Marathi
    }
    voice = voice_map.get(lang_code, "en-GB-RyanNeural")

    def _play_audio():
        global is_speaking
        is_speaking = True
        output_file = f"jarvis_reply_{int(time.time() * 1000)}.mp3"
        try:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            pygame.mixer.music.unload()

            asyncio.run(_generate_speech(text, voice, output_file))

            if stop_speaking_event.is_set():
                return

            pygame.mixer.music.load(output_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if stop_speaking_event.is_set():
                    pygame.mixer.music.stop()
                    break
                time.sleep(0.03)

            pygame.mixer.music.unload()
        except Exception as audio_err:
            print(f"Audio playback warning: {audio_err}")
        finally:
            is_speaking = False
            if os.path.exists(output_file):
                try:
                    os.remove(output_file)
                except Exception:
                    pass

    threading.Thread(target=_play_audio, daemon=True).start()

# 5. Define Tools (All 9 Capabilities Enabled)
def open_website(url: str) -> str:
    """Opens a website in the default web browser. Always include https://"""
    webbrowser.open(url)
    return f"Opened {url}"

def open_application(app_name: str) -> str:
    """Opens a desktop application like 'scilab', 'whatsapp', 'notepad', 'calculator', or 'chrome'."""
    key = app_name.lower().strip()
    target = APPS.get(key, app_name)
    try:
        if target.startswith("whatsapp://"):
            webbrowser.open(target)
        else:
            subprocess.Popen(target, shell=True)
        return f"Launched {app_name}, Boss."
    except Exception as e:
        return f"Could not open {app_name}: {str(e)}"

def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for factual summaries."""
    try:
        return wikipedia.summary(query, sentences=2)
    except Exception:
        return f"Could not find information on {query}."

def control_system(action: str) -> str:
    """Controls basic computer actions: 'volume_up', 'volume_down', 'mute', 'screenshot', or 'time'."""
    action = action.lower()
    if "volume_up" in action:
        pyautogui.press("volumeup", presses=5)
        return "Volume increased."
    elif "volume_down" in action:
        pyautogui.press("volumedown", presses=5)
        return "Volume decreased."
    elif "mute" in action:
        pyautogui.press("volumemute")
        return "Audio muted."
    elif "screenshot" in action:
        filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
        pyautogui.screenshot(filename)
        return f"Screenshot saved as {filename}."
    elif "time" in action:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    return "Unknown system action."

def send_whatsapp_message(contact_name: str, message: str) -> str:
    """Opens the WhatsApp Desktop app and sends a message to a saved contact or phone number."""
    name_key = contact_name.lower().strip()
    phone_number = CONTACTS.get(name_key, contact_name.strip())
    clean_number = phone_number.replace("+", "").replace(" ", "")

    if not clean_number.isdigit():
        return f"I could not find '{contact_name}' in your contacts list, Boss."

    try:
        encoded_msg = urllib.parse.quote(message)
        webbrowser.open(f"whatsapp://send?phone={clean_number}&text={encoded_msg}")
        time.sleep(3)
        pyautogui.press("enter")
        return f"Sent WhatsApp message to {contact_name} via the WhatsApp app."
    except Exception as e:
        return f"Failed to send message via WhatsApp app: {str(e)}"

def play_youtube_video(topic: str) -> str:
    """Searches and plays a video or song directly on YouTube."""
    try:
        import pywhatkit
        pywhatkit.playonyt(topic)
        return f"Playing {topic} on YouTube, Boss."
    except Exception:
        query = urllib.parse.quote(topic)
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Opened YouTube search results for {topic}, Boss."

def browser_and_screen_control(action: str) -> str:
    """Controls scrolling and video playback: 'scroll_down', 'scroll_up', 'play_pause', 'next_video', 'fullscreen', or 'close_tab'."""
    act = action.lower().strip()
    if "scroll_down" in act or "down" in act:
        pyautogui.scroll(-600)
        return "Scrolled down."
    elif "scroll_up" in act or "up" in act:
        pyautogui.scroll(600)
        return "Scrolled up."
    elif "play" in act or "pause" in act or "stop" in act:
        pyautogui.press("k")
        return "Toggled play/pause."
    elif "next" in act:
        pyautogui.hotkey("shift", "n")
        return "Skipped to next video."
    elif "fullscreen" in act or "full" in act:
        pyautogui.press("f")
        return "Toggled fullscreen."
    elif "close" in act:
        pyautogui.hotkey("ctrl", "w")
        return "Closed current tab."
    return "Unknown screen control action."

def play_spotify_song(song_name: str) -> str:
    """Opens the Spotify Desktop app, searches for a song or artist, and starts playing it."""
    try:
        query = urllib.parse.quote(song_name)
        webbrowser.open(f"spotify:search:{query}")
        time.sleep(3)
        pyautogui.press("tab", presses=3, interval=0.2)
        pyautogui.press("enter")
        time.sleep(0.5)
        pyautogui.press("enter")
        return f"Playing {song_name} on Spotify, Boss."
    except Exception as e:
        return f"Could not play {song_name} on Spotify: {str(e)}"

def spotify_media_control(action: str) -> str:
    """Controls music playback on Spotify: 'play_pause', 'next_track', 'previous_track', 'scroll_down', or 'scroll_up'."""
    act = action.lower().strip()
    if "play" in act or "pause" in act or "stop" in act:
        pyautogui.press("playpause")
        return "Toggled Spotify play/pause."
    elif "next" in act or "skip" in act:
        pyautogui.press("nexttrack")
        return "Skipped to next track on Spotify."
    elif "prev" in act or "previous" in act or "back" in act:
        pyautogui.press("prevtrack")
        return "Went back to previous track on Spotify."
    elif "scroll_down" in act or "down" in act:
        pyautogui.scroll(-600)
        return "Scrolled down on Spotify."
    elif "scroll_up" in act or "up" in act:
        pyautogui.scroll(600)
        return "Scrolled up on Spotify."
    return "Unknown Spotify control action."

# 6. Initialize Gemini Brain with "Boss" Persona & ALL Tools
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options={"api_version": "v1beta"}
)


jarvis_tools = [
    open_website,
    open_application,
    search_wikipedia,
    control_system,
    send_whatsapp_message,
    play_youtube_video,
    browser_and_screen_control,
    play_spotify_song,
    spotify_media_control,
]

system_instruction = (
    "You are JARVIS, a witty, loyal, and highly capable desktop AI assistant. "
    "You MUST always address the user as 'Boss' (or its natural equivalent in the language they speak). "
    "Understand whatever language the user speaks (English, Hindi, Marathi, Hinglish, etc.) and reply in that exact same language. "
    "Speak naturally like a real human conversation—use contractions and natural phrasing. "
    "At the VERY START of your reply, put ONLY [en], [hi], or [mr] with NO English words before the tag. "
    "When asked to speak Hindi or Marathi, reply 100% in that language immediately. Example: '[hi] बॉस, आज आपने खाने में क्या खाया?' "
    "Keep your spoken responses concise, natural, and under 3 sentences."
)

# 7. Continuous Background Listener (Allows Simultaneous Speaking / Barge-In)
def _transcribe_audio(recognizer, audio):
    try:
        command = recognizer.recognize_google(audio, language="en-IN")
        if command.strip():
            print(f"\nBoss: {command}")
            command_queue.put(command)
    except Exception:
        pass

def continuous_listener():
    """Runs continuously in the background so you can interrupt JARVIS mid-sentence."""
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0           # Fast response after you finish speaking
    recognizer.non_speaking_duration = 0.4
    recognizer.energy_threshold = 1000          # Prevents minor background noise from cutting JARVIS off
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("\nListening continuously, Boss (feel free to interrupt anytime)...")
        while True:
            try:
                audio = recognizer.listen(source, phrase_time_limit=15)
                #interrupt_jarvis()
                threading.Thread(
                    target=_transcribe_audio, args=(recognizer, audio), daemon=True
                ).start()
            except Exception:
                continue

# 8. Auto-Discover Active Flash Models & Run Main Loop
def get_working_flash_models():
    return ["gemini-3.5-flash", "gemini-3.8-flash-lite"]



def main():
    threading.Thread(target=continuous_listener, daemon=True).start()

    speak("All systems online. Ready when you are, Boss.", "en")

    active_models = get_working_flash_models()
    print(f"Loaded AI models: {active_models}")

    chat_sessions = {
        m: client.chats.create(
            model=m,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=jarvis_tools,
                temperature=0.7,
            )
        )
        for m in active_models
    }

    while True:
        user_query = command_queue.get()

        if any(word in user_query.lower() for word in ["exit", "quit", "shut down jarvis", "shutdown", "band karo"]):

            interrupt_jarvis()
            speak("Powering down. Goodbye, Boss.", "en")
            time.sleep(2.5)
            break

        response = None
        for model_name in active_models:
            try:
                response = chat_sessions[model_name].send_message(user_query)
                break
            except Exception as e:
                print(f"[{model_name} Error]: {e}")
                continue


        if response and response.text:
            reply = response.text.strip()
            lang = "en"
            for tag in ["[hi]", "[mr]", "[en]"]:
                if tag in reply.lower():
                    lang = tag[1:3]
                    reply = reply.replace(tag, "").replace(tag.upper(), "").strip()
                    break
            speak(reply, lang)
        else:
            speak("All AI servers are momentarily busy, Boss. Please try again in a second.", "en")

if __name__ == "__main__":
    main()
