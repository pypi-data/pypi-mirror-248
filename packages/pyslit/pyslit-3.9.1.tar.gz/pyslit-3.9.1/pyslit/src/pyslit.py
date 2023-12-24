# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 22:50:32 2023

@author: Ashraq
"""
def size(sequence,index=None,element=None,balance=False):
    l = 0
    for i in sequence:
        l+=1

    if balance == False:
        if index != None:
            if index > l:
                return l
            if index < 0:
                index += l
                if index < 0:
                    return l
            l = index                                      #Does not consider the given element
        elif element != None:
            l = 0
            for i in sequence:
                if i == element:
                    break
                l+=1
        else:
            pass

    else:
        if index != None:
            if index > l:
                return l
            if index < 0:
                index += l
                if index < 0:
                    return l
            l -= index                               #Consider the given element
        elif element != None:
            h = 0
            for i in sequence:
                if i == element:
                    break
                h+=1
            l -= h
        else:
            pass
    return l

def edit(sequence,index,char):                 #Dictionary
    if type(sequence) == dict:
        if index not in sequence:
            return sequence
        else:
            sequence[index] = char
            return sequence

    length = (len(sequence)-1)
    n_len = -len(sequence)
    if index > length:
        return sequence
    if length == -1:
        return sequence
    if n_len > index:
        return sequence

    t = type(sequence)
    sequence = list(sequence)

    sequence[index]=char
    if t == str:
        s = ''
        for i in sequence:
            s+=i
    elif t == tuple:
        s = tuple(sequence)
    else:
        s = sequence
    sequence = s
    return sequence

def remove(sequence,index=None):              #Dictionary
    if type(sequence) == dict:
        for i in sequence:
            if sequence[i] == index:
                del dict[i]
                return sequence

    if index == None:
        sequence = sequence[:-1]
    else:
        l = sequence[:index]
        r = sequence[index+1:]
        sequence = l+r
    return sequence

def remove_item(sequence,element,occurance=1):   #remove element at a particular occurance
    length = len(sequence)
    ele_len = len(element)
    h = 0
    l = sequence
    r = type(sequence)()
    for i in range(length):
        if element in sequence[i:ele_len]:
            h += 1
            l = sequence[:i]
            r = sequence[i+ele_len:]
        if h == occurance:
            break
    sequence = l+r
    return sequence

def remove_items(sequence,element,occurance=None):   #remove element for the number of times occurance
    ele_len = len(element)
    if occurance == None:
        occurance = len(sequence)
    l = ()
    r = ()
    h = 0
    e = 0
    for i in range(len(sequence)):
        while element in sequence[i:ele_len]:
            h += 1
            l = sequence[:i]
            r = sequence[i+ele_len:]
            sequence = l+r
            if (len(sequence)-1) < i:
                e = 1
                break
            if h == occurance:
                e = 1
                break
        if e == 1:
            break
    return sequence

def add(sequence,element,index=-1):
    t = type(sequence)
    sequence = list(sequence)
    element = [element]
    
    if index == -1:
        s = sequence+element
    elif index < -1:
        l = sequence[:index+1]
        r = sequence[index+1:]
        s = l+element+r
    else:
        l = sequence[:index]
        r = sequence[index:]
        s = l+element+r
        
    if t == str:
        S = ''
        for i in s:
            S+=i
        s = S
    elif t == tuple:
        s = tuple(s)
    else:
        pass
    sequence = s
    return sequence

def sort(array,reverse=False):
    t = type(array)
    array = list(array)
    for i in range(1, len(array)):
        key_item = array[i]
        j = i - 1
        if type(array[j]) != type(key_item):
            raise TypeError('Comparison not supported between different data types')
        while j >= 0 and array[j] > key_item:
            array[j + 1] = array[j]
            j -= 1
            if type(array[j]) != type(key_item):
                raise TypeError('Comparison not supported between different data types')
        array[j + 1] = key_item
    if reverse == True:
        r = []
        for k in range(len(array)-1,-1,-1):
            r += [array[k]]
        array = r
    else:
        pass
    if t == str:
        S = ''
        for i in array:
            S+=i
        array = S
    elif t == tuple:
        array = tuple(array)
    else:
        pass
    return array

def sort_alpha(sequence,first='alpha',reverse=False):
    t = type(sequence)
    sequence = list(sequence)
    alpha = []
    other = []
    for i in sequence:
        if type(i) == str:
            alpha += [i]
        else:
            other += [i]
    alpha = sort(alpha,reverse)
    if alpha == None:
        return
    if first == 'alpha':
        sequence = alpha+other
    else:
        sequence = other+alpha
    if t == str:
        S = ''
        for i in sequence:
            S+=i
        sequence = S
    elif t == tuple:
        sequence = tuple(sequence)
    else:
        pass
    return sequence

def sort_num(sequence,first='num',reverse=False):
    t = type(sequence)
    sequence = list(sequence)
    num = []
    other = []
    for i in sequence:
        if type(i) == int:
            num += [i]
        else:
            other += [i]
    num = sort(num,reverse)
    if num == None:
        return
    if first == 'num':
        sequence = num+other
    else:
        sequence = other+num
    if t == str:
        S = ''
        for i in sequence:
            S+=i
        sequence = S
    elif t == tuple:
        sequence = tuple(sequence)
    else:
        pass
    return sequence

def sort_all(sequence,first='num',reverse_alpha=False,reverse_num=False,reverse=False):
    t = type(sequence)
    sequence = list(sequence)
    alpha = []
    num = []
    for i in sequence:
        if type(i) == str:
            alpha += [i]
        else:
            num += [i]
    alpha = sort(alpha,(reverse_alpha or reverse))
    num = sort(num,(reverse_num or reverse))
    if (alpha == None) or (num == None):
        return
    if first == 'num':
        sequence = num+alpha
    else:
        sequence = alpha+num
    if t == str:
        S = ''
        for i in sequence:
            S+=i
        sequence = S
    elif t == tuple:
        sequence = tuple(sequence)
    else:
        pass
    return sequence

def index(sequence,element,l=0,r=None,occurance=1):
    if r == None:
        r = len(sequence)
    index = -1
    h = 0
    for i in range(l,r):
        if element in sequence[i:i+len(element)]:
            h += 1
            index = i
        if h == occurance:
            break
    return index

def index_all(sequence,element,l=0,r=None):
    if r == None:
        r = len(sequence)
    index = []
    for i in range(l,r):
        if element in sequence[i:i+len(element)]:
            index += [i]
    if len(index) == 0:
        index = -1
    return index
    
def isnum(sequence,l=0,r=None):
    if r == None:
        r = len(sequence)
    sequence = sequence[l:r]
    for i in sequence:
        if (ord(i) >= 48) and (ord(i) <= 57):
            return True
        else:
            continue
    return False

def isaplha(sequence,l=0,r=None):
    if r == None:
        r = len(sequence)
    sequence = sequence[l:r]
    for i in sequence:
        if ((ord(i) >= 65) and (ord(i) <= 90)) or ((ord(i) >= 97) and (ord(i) <= 122)):
            return True
        else:
            continue
    return False

def isalphanum(sequence,l=0,r=None):
    if r == None:
        r = len(sequence)
    sequence = sequence[l:r]
    for i in sequence:
        if (((ord(i) >= 65) and (ord(i) <= 90)) or ((ord(i) >= 97) and (ord(i) <= 122))) or ((ord(i) >= 48) and (ord(i) <= 57)):
            return True
        else:
            continue
    return False

def replace(sequence,element,replace,l=0,r=None,occurance=1):
    i = index(sequence,element,l,r,occurance)
    if i == -1:
        return sequence
    L = sequence[:i]
    R = sequence[i+len(element):]
    sequence = L+replace+R
    return sequence

def replaces(sequence,element,replace,l=0,r=None,occurance=1):
    i = index_all(sequence,element,l,r)
    if i == -1:
        return sequence
    i = i[:occurance]
    for j in i:
        L = sequence[:i[j]]
        R = sequence[i[j]+len(element):]
        sequence = L+replace+R
    return sequence

def replace_all(sequence,element,replace,l=0,r=None):
    i = index_all(sequence,element,l,r)
    if i == -1:
        return sequence
    for j in i:
        L = sequence[:i[j]]
        R = sequence[i[j]+len(element):]
        sequence = L+replace+R
    return sequence

def change_key(dict,key=None,value=None,n_key=None):
    if n_key == None:
        return dict
    if n_key in dict:
        raise KeyError('n_key is already present. Enter a new key')
    
    if key != None:
        for i in dict:
            if i == key:
                value = dict[key]
                del dict[i]
                dict[n_key] = value
                return dict
            else:
                pass
    else:
        for i in dict:
            if dict[i] == value:
                del dict[i]
                dict[n_key] = value
                return dict
            else:
                pass
    return dict

def get_key(dict,value=None,multiple=False):
    k = []
    for i in dict:
        if dict[i] == value:
            if multiple == False:
                return i
            else:
                k += [i]
    return k

def get_value(dict,key=None):
    if key == None:
        return dict
    for i in dict:
        if i == key:
            return dict[i]


#########################################################################################################

import sys
import requests
import pygame
import os
from bs4 import BeautifulSoup
import datetime
import time as t
import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import openai

def internet_check():
    url = 'https://www.google.com/'
    timeout = 8
    try:
        request = requests.get(url,timeout=timeout)
        return True
    except(requests.ConnectionError, requests.Timeout) as exception:
        return False

engine = pyttsx3.init()
voice = engine.getProperty('voices')
engine.setProperty('voices', voice[0].id)
engine.setProperty('rate', 200)
def voice_change(i):
    engine.setProperty('voices', voice[i].id)
def voice_speed(s):
    engine.setProperty('rate', s)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def init_mp3():
    pygame.mixer.init()
def quit_mp3():
    pygame.mixer.quit()
def music_volume(x):
    pygame.mixer.music.set_volume(x)
def ismp3playing():
    b=pygame.mixer.get_busy()
    return b
def play_music(mp3):
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(mp3)
    pygame.mixer.music.play()
def pause_music():
    pygame.mixer.music.pause()
def unpause_music():
    pygame.mixer.music.unpause()
def stop_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
def music_pos():
    pos = pygame.mixer.music.get_pos()
    return pos

listener = sr.Recognizer()
listener.pause_threshold = 1.2
def listen(entry=None):
    command = ''
    if entry!=None:
        with sr.Microphone() as source:
            speak('Listening')
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
        try:
            speak('Recognizing')
            command = listener.recognize_google(voice)
            command = command.lower()
        except:
            speak('Please check your internet connection and tell again')
            return None

    else:
        with sr.Microphone() as source:
            print("Listening.....")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
        try:
            print("Recognizing.....")
            command = listener.recognize_google(voice)
            command = command.lower()
        except:
            return 'Please check your internet connection and tell again'
    return command

def youtube(search):
    try:
        import pywhatkit as q
        q.playonyt(search)
        return 'Ok'
    except:
        return 'Please check your internet connection and try again'

def google(query):
    try:
        import pywhatkit as q
        q.search(query)
        return 'Ok'
    except:
        return 'Please check your internet connection and try again'

def wikipedia_s(search, sentences=2):
    if internet_check() == False:
        return "/*Pyslit: Please connect to internet!*/"
    result = wikipedia.summary(search, sentences)
    return result

def shutdown():
    os.system("shutdown /s /t 1")
def log_out():
    os.system("shutdown -l")
def restart():
    os.system("shutdown /r /t 1")
def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
def open_app(app):
    os.system(app)
def run_file(file):
    os.startfile(file)
def cmd(command):
    r = os.popen(command).readlines()
    try:
        for i in range(len(r)-1):
            if r[i] == '\n':
                del r[i]
                continue
            r[i] = r[i].strip('\n')
    except:
        return r
    return r

def news(website='https://www.thehindu.com/',count=5):
    news = ''
    try:
        response = requests.get(website, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        headlines = soup.find('body').find_all('h3')
        a = []
        for x in list(dict.fromkeys(headlines)):
            z = x.text.strip()
            a.append(z)
        for i in range(count):
            news += ', '+'\n'+str(a[i])
    except(requests.ConnectionError, requests.Timeout) as exception:
        return "/*Pyslit: Please connect to internet!*/"
    return news

def time():
    time = datetime.datetime.now().strftime("%I:%M %p")
    return time
def date():
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    return date
def day():
    day = datetime.datetime.now().strftime("%A")
    return day
def month():
    month = datetime.datetime.now().strftime("%B")
    return month

def web(link):
    if internet_check() == False:
        print("/*Pyslit: Please connect to internet!*/")
        return
    webbrowser.open(link)

def delay(seconds):
    t.sleep(seconds)

api_key = ''
messages = [{"role": "system", "content": "You are a intelligent assistant."}]
def ai(command):
    global messages
    if api_key == '':
        return "/*Pyslit: Please mention your API key!*/"
    openai.api_key = api_key
    try:
        messages.append({"role": "user", "content": command})
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply
    except:
        return '/*Pyslit: Error'
def create_image(image_name,directory):
    if api_key == '':
        return "/*Pyslit: Please mention your API key!*/"
    openai.api_key = api_key
    try:
        res = openai.Image.create(prompt=image_name,n=1,size="1024x1024")
        url = res["data"][0]["url"]
        response = requests.get(url).content
    except:
        return '/*Pyslit: Error'
    with open(f"{directory}/{image_name}.png", "wb") as f:
            f.write(response)
