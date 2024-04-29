# Student ID : 20212956
# Name : 구여진

import sys
from socket import *

def prompt():
    print("\n> ", end="", flush=True)

GETCMD = "down"
QUITCMD = "quit"

try:
    print("Student ID : 20212956")
    print("Name : Yeojin Goo")

    prompt() 

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                print("No input received.")
                exit(0)

            cmd = line.strip().split()[0]
            if not cmd:
                prompt()
                continue
            elif cmd.lower() == QUITCMD:
                exit(0)
            elif cmd.lower() != GETCMD:
                print(f"Wrong command {cmd}")
                prompt()
                continue
        
            # connect to a server
            # NEED TO IMPLEMENT HERE
            url = line.strip().split()[1]
            
            url_split = url.split('/')
            host = url.split('/')[2] 
            host = host.split(':')[0]
            path = '/' + '/'.join(url_split[3:])
            file_name = url_split[-1]
            scheme = url.split('://')[0]

            if scheme != "http": #http 아닐 때 - exception3
                print(f"Only support http, not {scheme}\n")
                continue
            
            # make socket
            cSocket = socket(AF_INET, SOCK_STREAM)
            
            # connect to server
            connect_s = cSocket.connect_ex((host, 80))
            
            if connect_s != 0: # connect failed - exception 1
                print(f"{host}: unknown host")
                print(f"cannot connect to server {host} 80\n")
                
            request_message = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nUser-agent: Hw1/1.0\r\nConnection: keep-alive\r\n\r\n"
            request_message1 = f"GET {path} HTTP/1.0\r\nHost: {host}\r\nUser-agent: Hw1/1.0\r\nConnection: keep-alive\r\n"
            print(request_message1)
            
            send_s = cSocket.send(request_message.encode('utf-8')) #get request 
            
            response_message = b""
            while True: #response message receive
                data = cSocket.recv(1024)
                if not data:
                    break
                response_message += data
            
            response_message_h = response_message.split(b'\r\n\r\n')[0]
            response_message_b = response_message.split(b'\r\n\r\n')[1]
            status = " ".join(response_message_h.decode().split('\r\n')[0].split(' ')[1:])  # 200 ok
            content_length = int(response_message_h.decode().split("Content-Length: ")[1].split("\r\n")[0])
            
            if status == "200 OK":
                print(f"Total Size {content_length} bytes")
                with open(file_name, 'wb') as f:
                    download_bytes = 0
                    pre_percent = 0
                    i = 0
                    while download_bytes < len(response_message_b):
                        if len(response_message_b) - download_bytes < 1024:
                            i = len(response_message_b)
                        else: i = download_bytes + 1024
                        data = response_message_b[download_bytes:i]
                        f.write(data)
                        download_bytes += len(data)
                        percent = int(download_bytes / content_length * 100)
                        if (percent //  10 - pre_percent // 10) >= 1:
                            print(f"Current Downloading {download_bytes}/{content_length} (bytes) {percent}%\n")
                        pre_percent = percent
                    print(f"Download Complete: {file_name}, {content_length}/{content_length}\n")
            else: # 200이 아닐 때 - exception 2
                print(status + '\n')
            
        except EOFError:
            print("An error occurred while reading input from stdin.")
            exit(1)

except KeyboardInterrupt:
    print("\nProgram interrupted.")
    exit(1)