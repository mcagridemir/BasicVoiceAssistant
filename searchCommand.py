import os
import speech_recognition as sr
import time
import subprocess
import locale
import sys

from gtts import gTTS
from pygame import mixer
from selenium import webdriver
from datetime import date


#This is our speak function, when speak("text") is triggered, this function apply text to speech by speak value.
def speak(soundString):
    print(soundString)
    tts = gTTS(text=soundString, lang='tr')
    tts.save("sound.mp3")
    #os.system("sound.mp3")

    #sound.mp3 is played
    mixer.init()
    mixer.music.load("sound.mp3")
    mixer.music.play()

#Local was set as TR for date speech.
locale.setlocale(locale.LC_ALL, 'tr_TR.utf-8')

#Within text that was gave to function, texts that were caught are checked whether be a command.
def assistant(data):
    #If you say "Merhaba", the app will say "Merhaba" to you.
    if "merhaba" in data:
        speak("Merhaba")
    #If you tell below commands, the app will say today's date.
    elif "tarih" in data:
        speak("Bugün günlerden " + date.today().strftime("%d %B %Y"))

    #If you tell "dur", the app will be terminated.
    elif "dur" in data:
        print("Durduruluyor...")
        sys.exit()

#function that listens to microphone
def recordSound():
    #recognizer is defined before listening microphone
    r = sr.Recognizer()
    #data is got from microphone in here
    with sr.Microphone() as source:
        print("Seni dinliyorum...")
        sound = r.listen(source)
    #here, google voice recognition system is used, internet necessary for this system.
    data = ""
    try:
        #recognizer language was set Turkish
        #also, upper or lower cases come according to voice tone, so texts were set as lower case
        data = r.recognize_google(sound, language='tr-tr').lower()

        #If "çal" word exists in phrase, command works
        if "çal" in data.split():
            #The phrase is divided into words again.
           data = data.split()
           #Here, words that preceded "çal", are assigned to musicName.
           #For example, if the phrase is "Barış Manço Çal", musicName is Barış Manço.
           musicName = ""
           for i in data[:-1]:
               musicName = musicName + i
           speak(musicName + " çalınacak")
           #Chrome is opened.
           driver = webdriver.Chrome(executable_path='/Users/cagridemir/Desktop/4th Year 1st Term/Natural Language Processing/voiceAssistant/chromedriver')
           #youtube link was created and musicName is added to the end of youtube link
           driver.get("https://www.youtube.com/results?search_query="+musicName);
           #Here, the item that will be clicked was appointed as video title.
           select_element = driver.find_elements_by_xpath('//*[@id="video-title"]')
           #Loop clicks to it.
           for option in select_element:
               option.find_element_by_xpath('//*[@id="video-title"]').click()

        #If you say "spotify'ı aç/spotify aç", spotify will be opened
        elif "spotify" and "aç" in data.split():
            speak("Spotify'ı açıyorum")
            spotifyDir = '/Applications/Spotify.app'
            subprocess.call(['open', spotifyDir])

        #If you tell related "dur", the app will be terminated.
        elif "dur" in data.split():
            print("Durduruluyor...")
            sys.exit()

        #If you do not say above commands, app will search in google your command.
        else:
            data = data.split()
            searchItem = ""
            for i in data[:-1]:
                searchItem = searchItem + i
            if searchItem != "":
                speak(searchItem + " için arama sonuçlarım şöyle")
                driver = webdriver.Chrome(executable_path='/Users/cagridemir/Desktop/4th Year 1st Term/Natural Language Processing/voiceAssistant/chromedriver')
                driver.get("http://www.google.com/search?q="+searchItem);

    #When redundant voices and noise come, this command works
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand sound")
    return data

#we wait 2 seconds and apply Text to Speech before starting the assistant.
time.sleep(2)
speak("Merhaba, Sana Nasıl Yardımcı Olabilirim?")

#Here, the app listens continuously.
#If you say "dur", the app will be terminated.
while 1:
    data = recordSound()
    assistant(data)
