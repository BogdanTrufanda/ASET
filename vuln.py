import subprocess


def searchsploit(keyword: str):
    subprocess.call(["searchsploit"] + keyword.split(" "))
