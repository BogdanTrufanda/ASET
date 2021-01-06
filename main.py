import PySimpleGUI as sg
import hasher
import brute
import fuzzer
import jwtdecoder
import race
import rshell
import serverscan
import tracker
import vuln
import osint
import threading



function_mappings = {
        "jwtdecoder.decode_jwt": jwtdecoder.decode_jwt,
        "fuzzer.fuzz_them": fuzzer.fuzz_them,
        "serverscan.nmap_scan": serverscan.nmap_scan,
        "vuln.searchsploit": vuln.searchsploit,
        "tracker.track_me": tracker.track_me
}


def create_sec_gui(text: str, button_text: str, window_text: str, fct_name: str):
    sg.theme('DarkAmber')
    layout = [  [sg.Text(text), sg.InputText()],[sg.Button(button_text), sg.Button('Cancel')] ]
    window = sg.Window(window_text, layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': 
            break
        else:
            threading.Thread(target=function_mappings[fct_name], args=(values[0],), daemon=True).start()
    window.close()


def create_initial_gui():
    sg.theme('Reddit')  
    layout = [[sg.Button('Decode JWT',size=(10, 2)), sg.Button('Reverse shell',size=(10, 2))], [sg.Button('Brute forcer',size=(10, 2)), sg.Button('HTTP Fuzzer',size=(10, 2))], [sg.Button('Race Condition',size=(10, 2)), sg.Button('Social Media Tracker',size=(10, 2))], [sg.Button('Password\ncracker',size=(10, 2)),sg.Button('OSINT',size=(10, 2))],[sg.Button('CVE finder',size=(10, 2)),sg.Button('Service\nscanner',size=(10, 2))],[sg.Button('Exit',size=(10, 2))]]
    window = sg.Window('Attack framework', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Password\ncracker':
            hasher.gui_pc_funct()
        elif event == "OSINT":
            osint.gui_osint_funct()
        elif event == 'Brute forcer':
            brute.gui_funct()
        elif event == 'Decode JWT':
            create_sec_gui("Enter JWT: ", "Decode", "JWT decoder", "jwtdecoder.decode_jwt")
        elif event == 'HTTP Fuzzer':
            create_sec_gui("Enter URL: ", "Fuzz", "HTTP Fuzzer", "fuzzer.fuzz_them")
        elif event == 'Service\nscanner':
            create_sec_gui("Enter Target: ", "Scan", "Server Scan", "serverscan.nmap_scan")
        elif event == "CVE finder":
            create_sec_gui("Enter Service: ", "Find", "CVE Finder", "vuln.searchsploit")
        elif event == 'Reverse shell':
            rshell.create_reverse_shell()
        elif event == 'Race Condition':
            race.race_condition()
        elif event == 'Social Media Tracker':
            create_sec_gui("Enter nickname", "Hunt", "Social Media Tracker", "tracker.track_me")
    window.close()


def main():
    create_initial_gui()

if __name__ == "__main__":
    main()