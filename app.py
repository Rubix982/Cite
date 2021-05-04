from socket import *
from socket import error as SocketError
import errno
import requests
import os
import os.path
import sys
import ssl
import urllib3
import random

from src.LFU import LFUCache
from src.LRU import lrucache

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

while 1:
    option_select = int(input('''
    1. Start server
    2. Add new domain to blacklist
    3. Remove domain from blacklist
    4. Exit
    '''))

    if option_select == 1:
        hostname = 'localhost'
        port = 9997
        port_addr = (hostname, port)
        LFU_CACHE_SIZE, LRU_CACHE_SIZE = 256, 256

        # Caching mechanisms
        # lru_cache = lrucache(LRU_CACHE_SIZE)
        # lfu_cache = LFUCache(LFU_CACHE_SIZE)

        # SSL context
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain('./.ssh/cert.pem', './.ssh/key.pem')

        # Create a server socket, bind it to a port and start listening
        tcpSerSock = socket(AF_INET, SOCK_STREAM)
        tcpSerSock.bind(port_addr)
        tcpSerSock.listen(1)

        tcpSerSock = context.wrap_socket(tcpSerSock, server_side=True)

        while 1:
            # Start receiving data from the client
            print('\n\nReady to serve...')
            tcpCliSock, addr = tcpSerSock.accept()
            print('Received a connection from:', addr)
            message = tcpCliSock.recv(4096).decode('utf-8', 'ignore')

            print(message)

            if len(message.split(' ')) > 0:
                if message.split(' ')[1] == 'http://detectportal.firefox.com/success.txt' or message.split(' ')[1] == 'incoming.telemetry.mozilla.org:443':
                    continue
            else:
                continue

            # Extract the filename from the given message
            if message.split(' ')[1].startswith('http') or message.split(' ')[1].startswith('https'):
                filename = message.split(' ')[1].split('//')[1]
            else:
                filename = message.split(':')[0].split(' ')[1]

            with open('blacklist.txt', mode='r') as file:
                for line in file:
                    if filename == line[0:-1]:
                        print(
                            'This is one of the blocked domains. Forbidden 403!\r\n')
                        continue

            if filename.endswith('txt'):
                extension = ''
            else:
                extension = 'html'

            filename = filename.replace('www.', '').replace('/', '.')

            response = requests.get(
                f"https://{filename}", verify=False)

            # # Check wether the file exist in the cache
            # cache_file_path = f"cache/{filename}.{extension}"

            # # START CACHING MECHANISM

            # # Actual variable to store the data in
            # response = None

            # # # Checking if the data exists in the LFU cache
            # if lfu_cache.get(filename) == -1:

            #     # Checking if the data exists in the LRU cache
            #     if lru_cache.get(filename) == None:

            #         # The data is neither in the LRU cache
            #         # and neither in the LFU cache

            #         # Thus, the answer is to receive data from the
            #         # origin server

            #         # Get the response from the origin server and
            #         # store it in the 'response' variable.
            #         # This is a requests object capable of including the
            #         # file headers and the content, both in type(str) and
            #         # type(bytes)
            #         response = requests.get(
            #             f"https://{filename}", verify=False)

            #     else:
            #         # This control flow means that the LRU cache contains
            #         # the desird key - the data exists in the LRU cache

            #         # Get the path of the lfu cache
            #         response_path = f'./cache/lru/{filename}.{extension}'

            #         # Variable to handle the storage of the received file data
            #         response = None

            #         # Reading and sending the received data from the file
            #         # to the variable 'data'
            #         with open(response_path, mode='r') as lru_file_path:
            #             data = lru_file_path.readlines()

            #         # Insert into the LFU Cache as well
            #         lfu_folder_size = len([name for name in os.listdir(
            #             './cache/lfu') if os.path.isfile(name)])

            #         # After getting the data from the folder
            #         # insert that data into the LFU cache as well

            #         # LFU folder cache size determination
            #         if lfu_folder_size < LFU_CACHE_SIZE:

            #             lfu_cache.put(filename, lfu_folder_size)

            #             # End of control flow for inserting data into the LFU cache

            #         else:
            #             # This control flow means that the LFU Folder is full
            #             # Till the desired capacity

            #             # Randomly pick a file from the './cache/lfu' folder
            #             file_to_delete = random.choice(
            #                 list(lfu_cache.node_for_key.values()))

            #             # Delete it in the folder
            #             os.remove(f'./cache/lfu/{file_to_delete}')

            #             # Remove the filename from the cache
            #             lfu_cache.node_for_key.pop(filename)

            #             # Set the lfu cache key to a value action
            #             lfu_cache.put(filename, lfu_folder_size)

            #             # Write to a file in the cache
            #             with open(f'./cache/lfu/{filename}.{extension}', mode='w') as lfu_file_path:
            #                 lfu_file_path.write(data)

            #             # End of else control flow for updating the LFU cache

            #         # End of if control flow for receiving data from the LRU cache

            #         lfu_path = f'./cache/lfu/{filename}.{extension}'

            # else:

            #     # Start of control flow for getting the data from the LFU cache

            #     response_path = f'./cache/lfu/{filename}.{extension}'

            #     with open(response_path, mode='r') as lfu_file_path:
            #         data = lfu_file_path.readlines()

            #     # End of control flow for getting the data from the LFU Cache

            # # END CACHING MECHANISM

            # with open(cache_file_path, mode='w') as file:
            #     file.write(response.text)

            tcpCliSock.send(
                b"CONNECT " + str.encode(message.split('\n')[-3].split(' ')[1].replace('\r', '')) + b" HTTP/1.1\r\n")
            tcpCliSock.send(b"HTTP/1.1 200 OK\r\n")

            for key, value in response.headers.items():
                print(key, value)
                tcpCliSock.send(str.encode(key) + b":" +
                                str.encode(value) + b"\r\n")

            # ProxyServer finds a cache hit and generates a response message
            tcpCliSock.send(b"\r\n")

            try:
                tcpCliSock.send(response.content + b"\r\n")
            except SocketError as e:
                if e.errno != errno.ECONNRESET:
                    print(f'Connection Reset By Peer! {filename} ')
                continue

            # Close the client and the server sockets
            tcpCliSock.close()
        tcpSerSock.close()
    elif option_select == 2:
        with open('blacklist.txt', mode='a') as file:
            new_domain_to_add_to_blacklist = str(
                input("Enter new domain to add in blacklist: "))
            print(f'New domain extracted as: {new_domain_to_add_to_blacklist}')
            file.write(f"{new_domain_to_add_to_blacklist},\n")
    elif option_select == 3:
        with open('blacklist.txt', mode='a') as file:
            new_domain_to_remove_from_blacklist = str(
                input("Enter new domain to remove from blacklist: "))
            print(
                f'To remove domain extracted as: {new_domain_to_remove_from_blacklist}')

            final_domains = []

            for line in file:
                if new_domain_to_add_to_blacklist != line[0:-1]:
                    final_domains.append(line[0:-1])

        with open('blacklist.txt', mode='w') as file:
            for domain in final_domains:
                file.writeline(f"{domain},\n")
    elif option_select == 4:
        print('Exiting. Take care!')
        sys.exit(0)
    else:
        print('Unknown selected option. Choose again')
