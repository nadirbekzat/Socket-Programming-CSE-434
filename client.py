import socket

HOST = ""
PORT = 9090

s = input()
y = s.split()
if y[0] == "open":
    HOST = y[3]

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((HOST, PORT))


client.send(s.encode('utf-8'))
print(client.recv(1024))