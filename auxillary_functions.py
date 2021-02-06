#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 00:20:19 2020

NAME:
    auxillary_functions - This module contains functions that are addon/supplementary features.

FILE:
    auxillary_functions.py

FUNCTIONS:
    play_sound
    check_spk
    speech_rec
    check_speech
    listen_text
    
Royalty free audio files obtained from https://www.dreamstime.com/
and https://freesound.org
    http://www.orangefreesounds.com/category/sound-effects/beep-sounds/
@author: donsam

"""
#pre-defined modules
import tkinter.ttk as ttk 
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
from functools import partial
import  pyttsx3 

#user-defined modules
import GUI_functions as gf


text = ' '

#Function to play ui sounds
def play_sound(filename):
    sound = AudioSegment.from_wav(filename)
    play(sound)
    

#Function to display progress of submission 
def progress_bar(main_win):
    style = ttk.Style()
    style.theme_use('clearlooks')
    style.configure('grey.Horizontal.TProgressbar', background='blue')
    bar = ttk.Progressbar(main_win, length=300, style='grey.Horizontal.TProgressbar', 
                                                      mode = "indeterminate")
    bar.grid(row = 9, column = 2, columnspan = 5)
    bar.start(10)
    

#Function for checking the key pressed 
def check_spk(text, ticker_symbols, symbol_list): 
    #recognised text is assigned to variable value
    value = text
    #it is converted to upper case
    value = value.upper()   
    # if there is nothing in the value string
    if value == '': 
        #then the list of ticker symbols is displayed as is
        data = ticker_symbols 
    #otherwise    
    else:
        #based on the string within value the list is matched, case-insensitive
        data = ticker_symbols[ticker_symbols.str.contains(value, case=False)]
    # update data in listbox
    gf.update_listbox(data, symbol_list)  


#Function to convert speech to text
def speech_rec(ticker_symbol_e, ticker_symbols, symbol_list):
    #user is intimated to speak
    print('Speak Now')
    #audio file is played to indicate recogniser activation
    play_sound('Speak.wav')
    #function for recognising is initialised
    r = sr.Recognizer()
    #the sound recognised is from microphone
    with sr.Microphone() as source:
        #the audio phrase is recognised for a time of 5 secons
        audio_text = r.listen(source, phrase_time_limit=5)
        #audio file is played to confirm speech recognition
        play_sound('Done.wav')
        print('Done')
        global text 
        
    #checking if recogniser method works
        try:
            # using google speech recognition the audio text is proccessed
            text = r.recognize_google(audio_text)
            #confirmation of speech to text processing
            print('Processing Speech to text ')
            #recognised voice is printed as text
            print(text)
            #the ticker symbol field is set to the recognised text
            gf.set_text(ticker_symbol_e, text)
            #update listbox based on recognised text
            check_spk(text, ticker_symbols, symbol_list)
        #if voice is not recognised           
        except:
              #audio file is played to confirm failed recognition 
              play_sound('Failed.wav')           
              print('Sorry, did not catch that, Please try again...')

#Function to display speak button  
def check_speech(main_win, ticker_symbol_e, ticker_symbols, symbol_list):
    #speak button
    speak_b = ttk.Button(main_win, text='Speak', command = partial(speech_rec, ticker_symbol_e, ticker_symbols, symbol_list))
    #speak button position on window
    speak_b.grid(row=1,column=5)
    
#Function to read aloud the text passed        
def listen_text(text):
    #initialising the python tts engine
    tts = pyttsx3.init()
    #passing the text to be spoken out
    tts.say(text)
    tts.runAndWait()
        
    