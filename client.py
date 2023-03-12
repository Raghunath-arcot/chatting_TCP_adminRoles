import socket as s
import threading as th

username = input("Enter your name: ")
if username == 'admin':
    password = input("Enter password for admin: ")

client = s.socket(s.AF_INET, s.SOCK_STREAM)
client.connect(('127.0.0.1', 12834))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread:
            break

        try:
            message = client.recv(1024).decode('ascii')
            if message == 'USER':
                client.send(username.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused! Your Password is Wrong")
                        stop_thread = True
                elif next_message == 'BAN':
                    print('Connection refused because of ban!')
                    client.close()
                    break
            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break

def write():
    while True:
        if stop_thread:
            break
        message = f'{username}: {input("")}'
        if message[len(username)+2:].startswith('/'):
            if username == 'admin':
                if message[len(username)+2:].startswith('/remove'):
                    client.send(f'REMOVE {message[len(username)+2+8:]}'.encode('ascii'))
                elif message[len(username)+2:].startswith('/ban'):
                    client.send(f'BAN {message[len(username)+2+5:]}'.encode('ascii'))
            else:
                print("Commands can only be executed by the admin!")
        else:
            client.send(message.encode('ascii'))

receive_thread = th.Thread(target=receive)
receive_thread.start()

write_thread = th.Thread(target=write)
write_thread.start()