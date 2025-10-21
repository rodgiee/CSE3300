from socket import *
import _thread as thread

'''
Using open() extract each line of the provided dictionary and return as a list of strings.
note: Should also ensure that \n is stripped to not confuse wildcard algorithm
'''
def file_to_list(txt_file):
    txt_list = []
    with open(txt_file, 'r') as f:
        for line in f:
            txt_list.append(line.rstrip('\n'))
    return txt_list



# convert dictionary file to a list
english_dictionary = file_to_list('wordlist.txt')

'''
For wildcard matching, we know a word matches if characters in both words:
    1. equal (ex. b = b, c = c)
    2. query has ? (? = all characters, ? = a, ? =b, ...)

Matching can be made by iterating through each character at the same index for both words and checking for differences.
We can also reduce checking by first checking if the lengths differ (ex. app?le could never equal to bee)
'''
def is_wildcard_match(query, word):
    # different length of both words implies that these words will not match
    if len(query) == len(word): 
        for i in range(len(query)): 
            if query[i] != word[i] and query[i] != '?': 
                return False
        return True
    return False

'''
Find all wildcard matches based on client query with english dictionary.
Needs to be in string format to be encoded for transmission.
'''
def dictionary_match(query, dictionary):
    matches_str = ''
    for word in dictionary:
        if is_wildcard_match(query, word): matches_str += word + '\n'
    return matches_str

'''
Client thread functionn to:
    1. decode client data
    2. find wildcard matches
    3. encode and send back to client wildcard matches
'''
def client_handler(connection_socket, addr):
    # ex. 127.0.0.1:12345
    client_address = str(addr[0]) + ':' + str(addr[1])

    print(f"🔗Connection established with {client_address}")
    
    # convert byte data into string data
    sentence = connection_socket.recv(1024).decode('utf-8')
    query_matches = dictionary_match(sentence, english_dictionary)
    connection_socket.send(query_matches.encode('utf-8'))

    connection_socket.close()
    print(f"⛓️‍💥Connection closed with {client_address}")

'''
Main function of TCP server, define the server socket and listen for incoming TCP connection requests.
Only accept up to 5 connections at a time and redirect client connections to client thread handlers.
'''
def tcp_server():

    # define and bind socket
    server_port = 12000
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(("",server_port))

    # ONLY ACCEPT 5 CONNECTIONS
    server_socket.listen(5)

    print("👂Wildcard Server is Listening...")

    # constantly listen for any new TCP connection requests
    while 1:
        connection_socket, addr = server_socket.accept()
        thread.start_new_thread(client_handler, (connection_socket, addr))


if __name__ == '__main__':
    tcp_server()
