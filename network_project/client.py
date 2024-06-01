# /create room1 : room1 이라는 메신저 세션을 만듦
# /invite user1 room1 : id가 user1인 사용자를 room1이라는 메신저 세션에 초대함
# /sendR room1 hello : room1이라는 메신저 세션에 hello라는 문구를 전송함
# /send user1 hello : id가 user1인 사용자에게 hello라는 문구를 전송함
# /del room1 : room1이라는 메신저 세션을 삭제함

import socket
from threading import Thread
import time

def recvMsg(sock, users):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
                if msg.startswith("<현재 접속 중인 User List>"):
                    parseUserList(msg, users)
                elif msg.startswith("invite"):
                    sock.send(f"new room {msg.split(' ', 1)[1]}".encode())
            else:
                break
        except:
            break

def parseUserList(msg, users):
    lines = msg.split('\n')[1:]
    for line in lines:
        if line.startswith("Id:"):
            nickname = line.split(": ")[1]
        elif line.startswith("IP:"):
            ip = line.split(": ")[1]
        elif line.startswith("Port:"):
            port = int(line.split(": ")[1])
            users[nickname] = (ip, port)

def loginToServer(server_ip, server_port, users):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))
    
    while True:
        msg = sock.recv(1024).decode()
        print(msg)
        if "닉네임을 입력하세요" in msg:
            nickname = input("=> ")
            sock.send(nickname.encode())
        elif "환영합니다." in msg:
            break
    
    recv_thread = Thread(recvMsg, args=(sock, users))
    recv_thread.daemon = True
    recv_thread.start()
    return sock

if __name__ == "__main__":
    users = {}
    cSocket = loginToServer("localhost", 8000, users)
    time.sleep(0.5) 

    print("-명령어 목록-")
    print("/create room1 : room1 이라는 메신저 세션을 만듦")
    print("/invite user1 room1 : id가 user1인 사용자를 room1이라는 메신저 세션에 초대함")
    print("/sendR room1 hello : room1이라는 메신저 세션에 hello라는 문구를 전송함")
    print("/send user1 hello : id가 user1인 사용자에게 hello라는 문구를 전송함")
    print("/del room1 : room1이라는 메신저 세션을 삭제함")
    
    while True:
        msgC = input()
        if msgC:
            cSocket.send(msgC.encode())
        time.sleep(0.5)
