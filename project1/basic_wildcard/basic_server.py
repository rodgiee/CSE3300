from socket import *

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
def tcp_server():
    
    # convert dictionary file to a list
    english_dictionary = file_to_list('wordlist.txt')

    # define and bind socket
    server_port = 12000
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(("",server_port))

    server_socket.listen(1)

    print("👂Wildcard Server is Listening...")

    while 1:
        connectionSocket, addr = server_socket.accept()

        # ex. 127.0.0.1:12345
        client_address = str(addr[0]) + ':' + str(addr[1])

        print(f"🔗Connection established with {client_address}")
        
        # convert byte data into string data
        sentence = connectionSocket.recv(1024).decode('utf-8')
        query_matches = dictionary_match(sentence, english_dictionary)
        connectionSocket.send(query_matches.encode('utf-8'))

        print(f"📩Message sent to {client_address}")
        connectionSocket.close()
        print(f"⛓️‍💥Connection closed with {client_address}")

if __name__ == '__main__':
    tcp_server()
