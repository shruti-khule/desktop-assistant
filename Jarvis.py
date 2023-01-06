import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser

from play_by_choices import *
from spotipy.oauth2 import SpotifyOAuth
import spotipy as sp

auth_manager = SpotifyOAuth(
    client_id="06c01e3d69d54064bf674a608ac7962f",
    client_secret="24c13affce3b4ace92c032f95c54e4bf",
    redirect_uri="http://localhost:8888/callback",
    username="315vehk7bi6zgrnndan7vvpban6q")

spotify = sp.Spotify(auth_manager=auth_manager)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    print(hour)
    if 4 <= hour <= 11:
        speak("Good Morning!")
    elif 11 < hour <= 16:
        speak("Good Afternoon!")
    elif 16 < hour <= 19:
        speak("Good Evening!")
    else:
        speak("Good Night!")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"User said : {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please!")
        return "None"
    return query


if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

        if "wikipedia" in query:
            speak("searching wikipedia...")
            query = query.replace("wikipedia", " ")
            results = wikipedia.summary(query, auto_suggest=False,  sentences=2)
            speak("According to Wikipedia..")
            speak(results)
        elif "open youtube" in query:
            webbrowser.open("youtube.com")
        elif "open google" in query:
            webbrowser.open("google.com")

        elif "play" in query:

            words = query.split()
            name = ' '.join(words[2:])

            print(words)
            print(name)

            if words[1] == 'album':
                uri = get_album_uri(spotify=spotify, name=name)
                play_album(spotify=spotify, device_id=deviceID, uri=uri)

            elif words[1] == 'artist':
                uri = get_artist_uri(spotify=spotify, name=name)
                play_artist(spotify=spotify, device_id=deviceID, uri=uri)

            elif words[1] == 'track':
                uri = get_track_uri(spotify=spotify, name=name)
                play_track(spotify=spotify, device_id=deviceID, uri=uri)
            else:
                print("please specify")
