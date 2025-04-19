
import pyttsx3
engine = pyttsx3.init() # object creation

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        #printing current voice rate
vRate = 180                       
engine.setProperty('rate', vRate)     # setting up new voice rate

"""VOLUME"""                       #printing current volume level
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. 1 for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 0 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(vRate))
engine.runAndWait()
engine.stop()

"""Saving Voice to a file"""
# On linux make sure that 'espeak' and 'ffmpeg' are installed
engine.save_to_file('Hello World', r'C:\Users\garym\Documents\GitHub\GaryManleyDataNew\AudioStuff\test.mp3')
engine.runAndWait()