from gtts import gTTS
from playsound import playsound
import datetime
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import random
import smtplib


def speak(text):
    """
    This function speaks whatever is given as the argument
    """
    try:
        audio = gTTS(text=text, lang='en')
        file = "voice.mp3"
        audio.save(file)
        playsound(file)
        os.remove(file)
        
    except Exception as e:
        print(f"Error in speak(): {e}")


def greeting():
    """
    This function greets the user depending on the time and introduces the AI to the user
    """
    hour = int(datetime.datetime.now().hour)

    if 0 <= hour < 12:
        speak("Good morning, boss!") 

    elif 12 <= hour < 18:
        speak("Good afternoon, boss!")

    else:
        speak("Good evening, boss!")

    speak("I am Jarvis, your personal AI assistant. How may I help you today?")


def voice_input():
    """
    This function takes an audio input from the user and saves it as query
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening to your command...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing your command...")
        query = r.recognize_google(audio, language="en-us")
        print(f"User said: {query}\n")

    except Exception:
        print("I'm sorry, I didn't quite understand that. Repeat your command please...")
        return "None"

    return query


def music_path():

    if os.path.exists("music_path.txt"):

        with open("music_path.txt", "r") as f:

            m_path = f.read().strip()

            if os.path.exists(m_path):
                return m_path
            else:
                speak("Saved path doesn't exist anymore.")

    speak("Assign a new music path.")
    m_path = input("Enter your music folder path (double slashes please): ").strip()

    if os.path.exists(m_path):

        with open("music_path.txt", "w") as f:
            f.write(m_path)

        return m_path
    
    else:
        speak("Invalid path.")
        return music_path()
    
    
def code_path():

    if os.path.exists("code_path.txt"):

        with open("code_path.txt", "r") as f:

            c_path = f.read().strip()

            if os.path.exists(c_path):
                return c_path
            else:
                speak("Saved path doesn't exist anymore.")

    speak("Assign a new code path.")
    c_path = input("Enter your code.exe folder path (double slashes please): ").strip()

    if os.path.exists(c_path):

        with open("code_path.txt", "w") as f:
            f.write(c_path)

        return c_path
    
    else:
        speak("Invalid path.")
        return code_path()
    
    
def login_email():

    if os.path.exists("email_address.txt"):

        with open("email_address.txt", "r") as f:

            email = f.read().strip()
            return email
        
    else:
        speak("No email address found.")

    speak("Provide an email address.")
    email = input("Enter your email address: ").strip()

    with open("email_address.txt", "w") as f:
        f.write(email)

    return email


def login_password():

    if os.path.exists("password.txt"):

        with open("password.txt", "r") as f:

            password = f.read().strip()
            return password
        
    else:
        speak("No password found.")

    speak("Provide a password.")
    password = input("Enter your password: ").strip()

    with open("password.txt", "w") as f:
        f.write(password)

    return password
    
   
    
def send_email(to, content):

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, content)
    server.close()

# Running the code

music_path()

code_path()

login_email()

login_password()

greeting()

while True:

    query = voice_input().lower()  # Makes the letters in the query to lowercase to search for specific words without worrying about case

    if "jarvis" in query:

        query = query.replace("jarvis","")

        if "wikipedia" in query:

            speak("Searching Wikipedia")
            query = query.replace("wikipedia", "") # Removes the word wikipedia from query to search the wikipedia for information on the query

            try:
                results = wikipedia.summary(query, sentences=2)
                print(results)
                print("")
                speak("According to Wikipedia," + results)

            except Exception as e:
                speak("Sorry, I couldn't find that on Wikipedia.")

        elif "open youtube" in query:

            webbrowser.open("youtube.com")

        elif "open google" in query:

            webbrowser.open("google.com")

        elif "open gmail" in query:

            webbrowser.open("gmail.com")

        elif "the time" in query:

            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Boss, the time is {time}")

        elif "play music" in query or "play some music" in query:

            m_path = music_path()

            songs = [i for i in os.listdir(m_path) if i.endswith(('.mp3'))]

            song = random.choice(songs)
            song_path = os.path.join(m_path, song)

            speak(f"Playing {song}")
            os.startfile(song_path)

        elif "open code" in query or "open coder" in query or "open my code" in query:

            c_path = code_path()
            c_exe = os.path.join(c_path, "Code.exe")
            os.startfile(c_exe)

        elif "send email" in query or "send mail" in query:

            email = login_email()
            password = login_password()

            try:

                speak("What should I send?")
                content = voice_input()

                speak("Please write the receiver's email address")
                to = input("To: ")

                send_email(to, content)
                speak("Email has been sent.")

            except Exception as e:

                print(e)
                speak("Sorry, boss. Invalid input.")

        elif "quit" in query or "bye" in query or "see you later" in query:
            
            speak("Goodbye")
            speak("Shutting down")
            break

    elif "quit" in query or "bye" in query or "see you later" in query:
            
        speak("Goodbye")
        speak("Shutting down")
        break

    else:
        speak("Please call me by my name")


    





    