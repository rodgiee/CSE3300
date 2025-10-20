from socket import *

def tcp_client():
    server_name = 'localhost'
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)

    client_socket.connect((server_name,server_port))

    sentence = input("send message: ")
    client_socket.send(sentence.encode())

    reply  = client_socket.recv(1024).decode('utf-8')
    print (f"From Wildcard Server, matches for '{sentence}' include:")
    print(reply)

    client_socket.close()

if __name__ == '__main__':
    tcp_client()
