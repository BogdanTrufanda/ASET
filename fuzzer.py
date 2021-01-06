import requests
from termcolor import colored



def fuzz_them(url_local: str):
    if url_local[-1] != "/":
        url_local += "/"
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


