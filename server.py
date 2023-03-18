import socket

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port
sock.bind(('localhost', 1234))
print("[RUNNING] The server is listening....")

# Define the database for storing customer information
# The keys are customer names and the values are tuples of (balance, IP address, portb, portp)
database = {}
database_checkpoint = {}

while True:
    # Receive a message from a customer
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    # Parse the message
    tokens = message.split()
    command = tokens[0]
    

    # Process the command
    if command == 'open':
        customer = tokens[1]
        balance = int(tokens[2])
        ip_address = tokens[3]
        portb = int(tokens[4])
        portp = int(tokens[5])

        if customer in database:
            response = 'FAILURE'
        else:
            database[customer] = (balance, ip_address, portb, portp)
            response = 'SUCCESS. Welcome to our bank!'

        # Send the response to the customer
        sock.sendto(response.encode(), addr)
        print("New customer has been added! \nName:" + tokens[1]+ "\nBalance: " + tokens[2] + "\nIP: " + tokens[3] + "\nPort1: "+ tokens[4]+ "\nPort2: " + tokens[5])
    elif command == 'new-cohort':
        customer = tokens[1]
        n = int(tokens[2])

        # Find n-1 other customers to form the cohort
        cohort = [customer]
        cohort_ips = [database[customer][1]] # List of IP addresses of cohort members
        for c in database:
            if c != customer:
                cohort.append(c)
                cohort_ips.append(database[c][1])
            if len(cohort) == n:
                break

        if len(cohort) == n:
            # Send the cohort information to each member of the cohort
            for ip_address in cohort_ips:
                response = 'SUCCESS. New cohort has been created!\n'
                for c in cohort:
                    response += '{} {} {}\n'.format(c, *database[c][1:])
                sock.sendto(response.encode(), (ip_address, database[customer][3]))
        else:
            response = 'FAILURE'
        print("New cohort with Adam, Beka, Maulen has been created!")

        # Send the response to the customer
        sock.sendto(response.encode(), addr)

    elif command == 'delete-cohort':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            cohort = [c for c in database if c != customer]

            # Send a message to each member of the cohort to delete the checkpoints
            for c in cohort:
                ip_address, portp = database[c][1], database[c][3]
                message = 'delete {}\n'.format(customer)
                sock.sendto(message.encode(), (ip_address, portp))

            # Delete the cohort from the database
            del database[customer]

            response = 'COHORT has been deleted!'
        print("Cohort with Adam, Beka, Maulen has been deleted")
        # Send the response to the customer
        sock.sendto(response.encode(), addr)

    elif command == 'deposit':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            amount = int(tokens[2])
            balance, ip_address, portb, portp = database[customer]
            balance += amount
            database[customer] = (balance, ip_address, portb, portp)
            response = 'SUCCESS. Your balance is ' + str(balance)
        print(customer + "'s new balance is "+str(balance))
    # Send the response to the customer
        sock.sendto(response.encode(), addr)

    elif command == 'withdrawal':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            amount = int(tokens[2])
            balance, ip_address, portb, portp = database[customer]
            if amount > balance:
                response = 'FAILURE'
            else:
                balance -= amount
                database[customer] = (balance, ip_address, portb, portp)
                response = 'SUCCESS. Your balance is ' + str(balance)
        print(customer + "'s new balance is "+str(balance))
    # Send the response to the customer
        sock.sendto(response.encode(), addr)
    
    elif command == 'balance':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            balance, ip_address, portb, portp = database[customer]
            response = 'Your balance is ' + str(balance)
        sock.sendto(response.encode(), addr)



    elif command == 'transfer':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            amount = int(tokens[2])
            label = tokens[4]
            balance, ip_address, portb, portp = database[customer]
            if amount > balance:
                response = 'FAILURE'
            else:
                balance -= amount
                database[customer] = (balance, ip_address, portb, portp)
                for c in database:
                    if c == tokens[3]:
                        balance, ip_address, portb, portp = database[c]
                        balance += amount
                        database[c] = (balance, ip_address, portb, portp)
                        response = 'Success, ' + customer + ' has transferred money to ' + c + '\n' + 'Label: ' + label

        print(response)
        sock.sendto(response.encode(), addr)

    elif command == 'lost-transfer':
        customer = tokens[1]
        if customer not in database:
            response = 'FAILURE'
        else:
            amount = int(tokens[2])
            label = tokens[4]
            balance, ip_address, portb, portp = database[customer]
            if amount > balance:
                response = 'FAILURE'
            else:
                balance -= amount
                database[customer] = (balance, ip_address, portb, portp)
                for c in database:
                    if c == tokens[3]:
                        balance, ip_address, portb, portp = database[c]
                        database[c] = (balance, ip_address, portb, portp)
                        response = 'Transfer lost, ' + customer + ' has transferred money to ' + c + ' but transfer was lost' + '\n' + 'Label: ' + label

        print(response)
        sock.sendto(response.encode(), addr)

    elif command == 'checkpoint':
        database_checkpoint = database.copy()
            
        response = "Checkpoint has been executed"
        print(response)
        sock.sendto(response.encode(), addr)

    elif command == 'rollback':
        database = database_checkpoint.copy()
            
        response = "Rollback has been executed"
        print(response)
        sock.sendto(response.encode(), addr)

    elif command == 'exit':
        if customer not in database:
            response = 'FAILURE'
        else:
            # Delete the customer's account information
            del database[customer]

            response = 'The program will close shortly...'

        # Send the response to the customer
        sock.sendto(response.encode(), addr)
        False 

    else:
        response = 'ERROR.The command is not found'

        # Send the response to the customer
        sock.sendto(response.encode(), addr)
