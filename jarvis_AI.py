import speech_recognition as sr
import pyttsx3
import webbrowser
import music_leb  # Your custom song link dictionary
import requests
import ollama
import os 
# --- Setup ---
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")


def speak(text):
    print("jarvis:", text)
    engine.say(text)
    engine.runAndWait()


def ask_ollama(question):
    print("Sending to Ollama:", question)
    try:
        response = ollama.chat(
            model="gemma:2b",
            messages=[
                {
                    "role": "system",
                    "content": "You are Jarvis, a custom AI assistant built by kira. Always speak confidently, briefly, and never say you are a Google model. Be personal and helpful.",
                },
                {"role": "user", "content": f"{question}. Reply in 2 lines only."},
            ],
        )

        return response["message"]["content"]
    except Exception as e:
        return "Sorry, I'm having trouble connecting to AI right now."


def processcommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif c.startswith("play"):
        song = c.split(" ", 1)[1]
        link = music_leb.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    elif "news" in c:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"
        )
        if r.status_code == 200:
            for article in r.json().get("articles", [])[:3]:
                speak(article["title"])
    elif "close the function" in c or "close" in c:
        speak("Your task ended successfully.")
        exit()

    else:
        # If command doesn’t match anything above, send to Ollama
        reply = ask_ollama(c)
        speak(reply)


# --- Main Loop ---
if __name__ == "__main__":
    speak("jarvis Here !")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()

            if "jarvis" in text:
                speak("Yes boss?")
                with sr.Microphone() as source:
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio).lower()
                    print("Command Recieved : ",command)
                processcommand(command)

        except Exception as e:
            print(f"Error: {e}")
