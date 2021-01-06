import PySimpleGUI as sg
import hashlib



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