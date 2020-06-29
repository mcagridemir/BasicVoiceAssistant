import os
import speech_recognition as sr
import time
import sys
import smtplib

from gtts import gTTS
from pygame import mixer

#This is our speak function, when speak("text") is triggered, this function apply text to speech by speak value.
def speak(msoundString):
    print(msoundString)
    tts = gTTS(text=msoundString, lang='tr')
    tts.save("msound.mp3")
    #os.system("sound.mp3")

    #sound.mp3 is played
    mixer.init()
    mixer.music.load("msound.mp3")
    mixer.music.play()

def sendMail():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        msound = r.listen(source)
    mailCommand = ""
    try:
        mailCommand = r.recognize_google(msound, language='tr-tr').lower()
        print(mailCommand + '\n')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand sound")
    return mailCommand

def run():
    try:
        #If you tell phrase that include mail/eposta words, you can send mail
        if 'eposta' or 'mail' in data:
            speak('Mailinizin konusu nedir?')
            time.sleep(1)
            #If you say "dur", app will be terminated.
            if sendMail() == "dur":
                print("Durduruluyor...")
                sys.exit()
            subject = sendMail()
            speak('Mailinizin mesaji nedir?')
            time.sleep(1)
            if sendMail() == "dur":
                print("Durduruluyor...")
                sys.exit()
            message = sendMail()
            content = 'Subject: {}\n\n{}'.format(subject, message).encode('utf-8')
            #init gmail SMTP
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            #identify to server
            mail.ehlo()
            #encrypt session
            mail.starttls()
            #login
            mail.login('youremail@gmail.com', 'youremailpassword')
            #send message
            mail.sendmail('youremail@gmail.com', 'targetemail@gmail.com', content)

            #end mail connection
            mail.close()
            speak('Mailiniz gönderildi.')
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand sound")

#we wait 2 seconds and apply Text to Speech before starting the assistant.
time.sleep(2)
speak("Merhaba, Sana Nasıl Yardımcı Olabilirim?")

#Here, the app listens continuously.
#If you say "dur", the app will be terminated.
while 1:
    data = run()
    assistant(data)
