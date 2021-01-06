import PySimpleGUI as sg
import requests
import json
import os
import socket
import re
import subprocess
import itertools
import threading
from termcolor import colored
import pprint



def valid_ip(ip: str) -> bool:
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def reverse_DNS(ip: str) -> bool:
    try:
        reversed_ip = socket.gethostbyaddr(ip)
        if "herokuapp" in reversed_ip[0]:
            return True
        else:
            return False
    except socket.error:
        return False


def valid_address(adress: str) -> (str, bool):
    if "herokuapp" not in adress:
        vi = valid_ip(adress)
        if vi:
            return ("Valid IP address!",reverse_DNS(adress))
        else:
            adress = adress.replace(".", "")
            if adress.isdigit():
                return ("Wrong IP format", False)
            else:
                return ("Wrong domain!", False)
    else:
        regex = re.findall(r'[:\/\-\.0-9A-Za-z]+\.com(?:[\/|:][:#\.\/a-zA-Z0-9]*)?', adress)[0]
        if regex != adress:
            return ("Wrong domain", False)
        return ("Match domain", True)


def is_json(myjson: str) -> bool:
    try:
        json.loads(myjson)
        return True
    except:
        return False


def requester(endpoint: str, method: str, wordlist: str, payload: str, headers: str, cookies: str):
    if "http" not in endpoint:
        endpoint = "http://" + endpoint
    with open(wordlist, "r") as fd:
        content = fd.read()
    content = content.split("\n")
    if headers:
        headers = {}
    if cookies:
        cookies = {}
    for x in content:
        new_payload = json.loads(payload.split("|")[0])
        new_payload[payload.split("|")[1].strip(" ")] = x
        r = requests.post(endpoint, data=new_payload,
                        headers=headers, cookies=cookies)
        yield x, r.status_code



def create_gui() -> (list, sg.PySimpleGUI.Window):
    radio_choices = ['GET', 'POST', 'PUT', 'PATCH']
    sg.theme('DarkAmber')
    layout = [[sg.Text('Endpoint')], [sg.InputText(size=(80, 10))],
            [sg.Text('Method')], [sg.Radio(text, 1) for text in radio_choices],
            [sg.Text('Payload (also supply the value you want to replace after | )')], [
        sg.InputText(size=(80, 10))],
        [sg.Text('Headers')], [sg.InputText(size=(80, 10))],
        [sg.Text('Cookies')], [sg.InputText(size=(80, 10))],
        [sg.Text('Give word for leet')],[sg.InputText(size=(30, 10))], [sg.Button('Leet it')],
        [sg.Text('Chars, min, max')],[sg.InputText(size=(30, 10))], [sg.Button('Combine it')],
        [sg.Text('Wordlist')], [sg.FileBrowse(), sg.InputText(size=(68, 10))],
        [sg.Button('Launch Attack'), sg.Button('Clear')],
        [sg.Multiline(size=(64, 30), font=('Courier New', 12), disabled=False,  background_color='grey20', pad=(15, (15, 15)), key='textbox', autoscroll=True)]]
    return radio_choices, sg.Window('Python Brute_Forcer', layout, size=(630, 900))
    



def leet_words(word: str) -> list:
    replacers = {'o': '0', 'l': '1', 'i': '1', 'z': '2', 'e': '3',
               'a': '4', 's': '5', 'g': '6', 't': '7', 'b': '8', 'g': '9', 'a': '@'}
    combs = []
    for x in word.lower():
        leet_char = replacers.get(x, x)
        combs.append((x,) if leet_char == x else (x, leet_char))
    return [''.join(x) for x in itertools.product(*combs)]


def upper_leet(combo: str) -> list:
    return list(map(''.join, itertools.product(*(sorted(set((x.upper(), x.lower()))) for x in combo))))


def create_leets(word: str):
    long_list = []
    for x in leet_words(word):
        long_list.extend(upper_leet(x))
    with open("leet_word.txt", "w") as fd:
        for x in long_list:
            fd.write(x + '\n')


def leet_it(word: str):
    create_leets(word)


def combine_it(combo: list):
    subprocess.Popen(f"crunch {int(combo[1])} {int(combo[2])} {combo[0]} -o combined.txt", shell=True)

def gui_funct():
    radio_choices, window = create_gui()
    strok = ""
    nr = 1
    while True:
        event, values = window.read()
        method = None
        if event == None:
            break
        if event == "Clear":
            strok = ""
            nr = 1
            window['textbox'].update("")
            window.Refresh()
        if event == "Combine it":
            arg = values[9].split(" ")
            if len(arg) == 3:
                if arg[1].isdigit() and arg[2].isdigit() and arg[1] <= arg[2]:
                    combine_it(arg)
            else:
                window['textbox'].update("Only 3 blocks allowed/ Min and Max must be positive integers/ Max must be equal or higher than min!")
                window.Refresh()
        if event == "Leet it":
            if values[8] and values[8].isalpha():
                leet_it(values[8])
            else:
                window['textbox'].update("No empty string/ Only letters allowed!")
                window.Refresh()
        if event == "Launch Attack":
            for x in range(1, 5):
                if values[x] == True:
                    method = radio_choices[x-1]
                    break
            if values[0] == "" or values['Browse'] == "" or method == None or values[5] == "":
                window['textbox'].update("Fill all the inputs!")
                window.Refresh()
            else:
                window['textbox'].update("")
                window.Refresh()
                msg, cap = valid_address(values[0])
                if cap == True and msg == "Match domain":
                    if len(values[5].split("|")) == 2:
                        if is_json(values[5].split("|")[0]):
                            if len(values[5].split("|")[0]) >= 1:
                                if len([x for x in json.loads(values[5].split("|")[0]) if x == values[5].split("|")[1].strip(" ")]) == 1:
                                    for value, status_code in requester(values[0], method, values["Browse"], values[5], values[6], values[7]):
                                        if value != "":
                                            strok += f"{nr}) {value} \t\t\t\t Status_code: {status_code}\n"
                                            window['textbox'].update(strok)
                                            window.Refresh()
                                            nr += 1
                                        if status_code == 200:
                                            strok += f"FOUND! It is {value}\n"
                                            window['textbox'].update(strok)
                                            window.Refresh()
                                            break
                            else:
                                window['textbox'].update("Given input not found in JSON")
                                window.Refresh()
                        else:
                            window['textbox'].update("Payload is not in JSON format")
                            window.Refresh()
                    else:
                        window['textbox'].update("Give correct format for payload!")
                        window.Refresh()
                else:
                    message = msg + "\t\t" + str(cap)
                    window['textbox'].update(message)
                    window.Refresh()
    window.close()
