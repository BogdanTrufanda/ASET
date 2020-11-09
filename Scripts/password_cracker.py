from urllib.request import urlopen
import hashlib

def sha1_generator(word):
    print("\nSHA1:")
    setpass = bytes(word, 'utf-8')
    hash_object = hashlib.sha1(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)


def md5_generator(word):
    print("\nMD5:")
    setpass = bytes(word, 'utf-8')
    hash_object = hashlib.md5(setpass)
    guess_pw = hash_object.hexdigest()
    print(guess_pw)


def sha1_decrypt(inputhash, pwlist):
    flag = 1
    for guess in pwlist.split('\n'):
        hashedguess = hashlib.sha1(bytes(guess, 'utf-8')).hexdigest()
        if hashedguess == inputhash:
            flag = 0
            print('The password is ', str(guess))
            input('Press enter to return to menu.\n')
            menu()
    if flag == 1:
        print('The hash is not SHA1 type or not in list\n')


def md5_decrypt(inputhash, pwlist):
    flag = 1
    for guess in pwlist.split('\n'):
        hashedguess = hashlib.md5(bytes(guess, 'utf-8')).hexdigest()
        if hashedguess == inputhash:
            flag = 0
            print('The password is ', str(guess))
            input('Press enter to return to menu.\n')
            menu()
    if flag == 1:
        print('The hash is not MD5 type or not in list\n')


def menu():
    print('1. SHA1 Hash Generator\n')
    print('2. MD5 Hash Generator\n')
    print('3. Hash Decryption\n')
    print('0. Exit program\n')


menu()


list_common_pw = str(urlopen('https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-10000.txt').read(), 'utf-8')
option = 9

while option != 0:
    option = int(input('Pick an option from the menu above\n'))
    if option == 1:
        password = str(input('Input the password you want to hash...\n>'))
        sha1_generator(password)
        input('Press enter to return to menu.\n')
        menu()
    elif option == 2:
        password = str(input('Input the password you want to hash...\n>'))
        md5_generator(password)
        input('Press enter to return to menu.\n')
        menu()
    elif option == 3:
        givenhash = str(input('Input the hash you want to search.\n'))
        sha1_decrypt(givenhash, list_common_pw)
        md5_decrypt(givenhash, list_common_pw)
    elif option == 0:
        break
