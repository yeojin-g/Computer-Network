from socket import *
import os
import sys
import mimetypes

def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} portnum")
        sys.exit(1)

    portnum = int(sys.argv[1])

    print("Student ID : 20212956")
    print("Name : Yeojin Goo")

    serverPort = portnum
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('localhost', serverPort))
    serverSocket.listen(1)

    while True:
        connectionSocket, addr = serverSocket.accept()
        requestM = connectionSocket.recv(3000).decode('utf-8').split('\r\n')
        
        requestline = requestM[0]
        userAgent = 0
        for a in requestM:
            if 'User-Agent' in a:
                userAgent = a
                break
        print(requestline)
        print(userAgent)
        print(str(len(requestM)-3) + " headers")  
        
        fileName = requestline.split(' ')[1][1:]
        
        if not os.path.exists(fileName):
           print(f"Server Error : No such file ./{fileName}!")
           print("HTTP/1.0 404 NOT FOUND\nConnection: close\nContent-Length: 0\nContent-Type: text/html") 
           continue
            
        with open(fileName, 'rb') as f:
            data = f.read()
            length = len(data)
            cType = mimetypes.guess_type(fileName)[0]
            respondM = f"HTTP/1.0 200 OK\nConnection: close\nContent-Length: {length}\nContent-Type: {cType}\n\n"
            print(respondM)
            connectionSocket.send(respondM.encode())
            connectionSocket.send(data)
        

if __name__ == "__main__":
    main()

