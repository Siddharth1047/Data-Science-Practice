import pyttsx3 
import speech_recognition as sr 
import datetime
from countryinfo import CountryInfo
from googlesearch import search
from bs4 import BeautifulSoup
import webbrowser
import wikipedia
import requests
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)  for male voice
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("I am Selena, Sir. Please tell me how may I help you")       

def takeCommand():
    #It takes audio input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:  
        print("Say that again please...")  
        return "None"
    return query

def search_wikipedia(query):
    words = query.split()
    topic_chosen = words.index('for') + 1
    topic = words[topic_chosen].capitalize()
    try:
        search_url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        paragraphs = soup.find_all('p')
        result = ' '.join([p.get_text().strip() for p in paragraphs[:2]])
        speak(result) 
    except requests.exceptions.RequestException as e:
        result = "An error occurred while fetching the page."
        print(result)
    except Exception as e:
        result = "No page found with that title."
        print(result)
        
wikipedia.set_lang("en")

def get_capital(query):
    words = query.split()
    country_index = words.index('of') + 1
    country = words[country_index].upper()
    print('Searching...')
    try:
        country_capital = CountryInfo(f'{country}')
        result = country_capital.capital()
        speak(f"Capital of {country} is {result}")
    except:
        speak("Sorry, I encountered an error")
        print(":(")
        
        
def location_finder(query):
    words = query.split()
    base_url = "https://www.google.com/maps/search/?api=1&query="
    location_catch = words.index('of') + 1
    location = ' '.join(words[location_catch:]).capitalize()
    print("Location will be shown on your browser...")
    location_url = base_url + location.replace(' ', '+')
    webbrowser.open(location_url)
     
        
if __name__ == "__main__":
    wishMe()
    while True:

        query = takeCommand().lower()

        if 'Hello' in query or 'hi' in query:
            speak('Hi, I am Selena')
            
        elif 'thank you' in query or 'thanks' in query:
            speak("You are welcome")
            
        elif 'wikipedia for' in query:
            search_wikipedia(query)
            
        elif 'created you' in query:
            speak("My creator is Lord Siddharth, to know more about him visit the below link.")
            print("https://www.linktr.ee/siddharthgov01")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open chat GPT' in query:
            webbrowser.open("chat.openai.com")
            
        elif 'capital of' in query:
            get_capital(query)
            
        elif 'location of' in query:
            location_finder(query)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")
            
        elif 'quit' in query or 'exit' in query:
            speak("Goodbye!")
            break
        
        elif 'search youtube for' in query:
            words = query.split()
            search_index = words.index('for') + 1
            search_query = ' '.join(words[search_index:])
            url = f'https://www.youtube.com/results?search_query={search_query}'
            webbrowser.open(url)

        else:
            print("No query matched")