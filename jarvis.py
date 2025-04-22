import speech_recognition as sr
import webbrowser
import pyttsx3
from googlesearch import search
import requests

# Initialize recognizer and voice engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Text-to-speech function
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to search and play a song on YouTube
def play_song(song_name):
    query = f"{song_name} site:youtube.com"
    try:
        for url in search(query, num_results=1):
            return url
    except Exception as e:
        print("Error finding song:", e)
        return None

# Function to get weather report
def get_weather(city):
    api_key = "418047e81039f3839b1bdba41f355232"  # Replace with your OpenWeatherMap API key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return f"City {city} not found."

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        return f"The weather in {city} is {weather} with a temperature of {temp}°C. It feels like {feels_like}°C."

    except Exception as e:
        return "Unable to get weather right now."

# Function to process commands
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("http://google.com")
    elif "open facebook" in c:
        webbrowser.open("http://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("http://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("http://linkedin.com")
    elif c.startswith("play"):
        song_name = c.replace("play", "").strip()
        link = play_song(song_name)
        if link:
            speak(f"Playing {song_name}")
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "weather in" in c:
        city = c.split("weather in")[-1].strip()
        report = get_weather(city)
        speak(report)
    elif "exit" in c or "stop" in c:
        speak("Goodbye!")
        exit()
    else:
        speak("Sorry, I didn't understand that command.")

# Main loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word 'Jarvis'...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                if word.lower() == "jarvis":
                    speak("Yes?")
                    print("Jarvis Activated...")
                    with sr.Microphone() as source:
                        recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        audio = recognizer.listen(source, timeout=5)
                        command = recognizer.recognize_google(audio)
                        print(f"Command received: {command}")
                        processCommand(command)
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError:
            print("Speech recognition service down.")
            speak("I'm having trouble connecting to the speech recognition service.")
        except Exception as e:
            print("Error:", e)
