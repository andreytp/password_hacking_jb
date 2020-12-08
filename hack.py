import socket
import sys


def pass_gen():
    dict = '_abcdefghijklmnopqrstuvwxyz1234567890'
    for el0 in dict:
        for el1 in dict:
            for el2 in dict:
                for el3 in dict:
                    for el4 in dict:
                        for el5 in dict:
                            for el6 in dict:
                                yield (el0 + el1 + el2 + el3 + el4 + el5 + el6).replace('_', '')


def hacking(host: str, port: str):
    with socket.socket() as client_socket:
        client_socket.connect((host, int(port)))
        attempt = 0
        passwords = set()
        for message in pass_gen():
            if message in passwords or len(message) == 0:
                continue
            passwords.add(message)
            client_socket.send(message.encode('utf8'))
            response = client_socket.recv(1024).decode('utf8')
            if 'Connection success!' in response:
                print(message)
                return
            attempt += 1
            # print(f'Attempt {attempt} password: {message}, result:{response}')


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(args)
        print("The script should be called with two arguments")
        exit(1)
    hacking(*args[1:])

