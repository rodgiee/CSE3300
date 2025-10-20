from socket import *

'''
Collect user input to see if provided message is included in the english dictionary based on wildcard matching.
    1. Define and bind port
    2. Collect user input
    3. Wait for reply and decode message
    4. Print based on if content was provided or not

Cases include:
    - Server unable to be connected to = HTTP 404 not found
    - Content was successfully delivered and provided = HTTP 200 OK
    - No content was sent back but connection successful = HTTP 204 No Content
'''
def tcp_client():
    server_name = 'localhost'
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)

    
    # Check if server is open
    try:
        client_socket.connect((server_name,server_port)) 
    except:
        raise ConnectionError('HTTP 404 not Found')



    # collect input and send
    # ensure lowercase and strip of excess white space
    sentence = input("send message: ").lower().strip()
    client_socket.send(sentence.encode())

    reply  = client_socket.recv(1024).decode('utf-8')
    if len(reply):
        print('HTTP 200 OK')
        print (f"From Wildcard Server, matches for '{sentence}' include:")
        print(reply)
    else:
        print('HTTP 204 No Content')

    client_socket.close()

if __name__ == '__main__':
    tcp_client()
