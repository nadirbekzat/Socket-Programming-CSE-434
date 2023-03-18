import socket

# Set up the socket connection with the server
server_ip = "127.0.0.1" # Replace with the IP address of the server
server_port = 1234 # Replace with the port number of the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # Get user input for the command to send to the server
    command = input("Enter command: ")

    # Send the command to the server
    client_socket.sendto(command.encode(), (server_ip, server_port))

    # Receive the response from the server
    response, address = client_socket.recvfrom(1024)

    # Decode and print the response
    print(response.decode())
