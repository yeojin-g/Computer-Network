# Student ID : 20212956 
# Name : 구여진
    
from socket import *
import sys

def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} portnum")
        sys.exit(1)

    portnum = int(sys.argv[1])

    print("Student ID : 20212956")
    print("Name : Yeojin Goo")

    serverPort = portnum
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('localhost',serverPort))
    serverSocket.listen(1)

    while True:
        connectionSocket, addr = serverSocket.accept()
        requestM = connectionSocket.recv(3000).decode('utf-8').split('\r\n')
        #print(requestM[0])
        #print(requestM[1])
        print(requestM)
        
if __name__ == "__main__":
    main()
