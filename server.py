from cmath import isclose
import socket
import random

HOST = ''
PORT = 9090

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST, PORT))


#main code
class ClientInfo:
    def __init__(self, name, balance, ipAdd, portNum, clientPortNum, cohortStatus, clientAddress):
        self.name = name
        self.balance = balance
        self.ipAdd = ipAdd
        self.portNum = portNum
        self.clientPortNum = clientPortNum
        self.cohortStatus = "False"
        self.clientAddress = clientAddress

clientList = []
#main code end

server.listen(5)

while True:
    communication_socket, address = server.accept()
    print(f"COnnected to {address}")
    message = communication_socket.recv(1024).decode('utf-8')
    print(f"Message from client is: {message}")

    firstWordCommandLine = "111"
    while firstWordCommandLine != "exit":
        x = message.split()
        firstWordCommandLine = x[0]
        if firstWordCommandLine == "open":
            if len(x) != 6:
                print("Failure, wrong command format")
            else:
                isClientAlreadyThere = "False"
                name = x[1]
                balance = x[2]
                ipAdd = x[3]
                portNum = x[4]
                clientPortNum = x[5]
                theInfo = ClientInfo(name, balance, ipAdd, portNum, clientPortNum, "False", address)
                for m in clientList:
                    if theInfo.name == m.name:
                        isClientAlreadyThere = "True"
                if isClientAlreadyThere == "False":
                    clientList.append(theInfo)
                    print("The User has been Added")
                    communication_socket.send(f"SUCCESS".encode('utf-8'))
                    communication_socket.close()
                else:
                    print("The User has NOT been Added")
                    communication_socket.send(f"FAILURE, This User Already Exists".encode('utf-8'))
                    communication_socket.close()

        elif firstWordCommandLine == "new-cohort":
            if len(x) != 3:
                print("Failure, wrong command format")
                communication_socket.send(f"FAILURE, wrong format".encode('utf-8'))
            elif int(x[2]) > len(clientList):
                print("Failure, wrong command format")
                communication_socket.send(f"FAILURE, size too big".encode('utf-8'))
            else:
                isNameCohort = "False"
                name = x[1]
                n = x[2]
                cohort = []
                for m in clientList:
                    if m.name == name:
                        isNameCohort = "True"
                        cohort.append(m)
                        m.cohortStatus = "True"
                if isNameCohort == "False":
                    print("The User has NOT been Added")
                    communication_socket.send(f"FAILURE, There is no such User".encode('utf-8'))
                cohortCounter = 0
                while cohortCounter != (int(n)-1):
                    v = random.choice(clientList)
                    if v.cohortStatus == "False":
                        cohort.append(v)
                        cohortCounter = cohortCounter + 1
                print("The new cohort has been created")
                communication_socket.send(f"SUCCESS, you were added to cohort".encode('utf-8'))
                for m in cohort:
                    print(m.name)
        elif firstWordCommandLine == "delete-cohort":
            print("The cohort has been deleted")
            communication_socket.send(f"SUCCESS, you were deleted from cohort".encode('utf-8'))         
        
        firstWordCommandLine = "exit"
                


    
    print(f"connection with {address} ended!")


    for m in clientList:
        print(m.name)
        


