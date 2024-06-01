import socket
import threading

# 접속 유저 관리
users = {} # user 정보 목록
clients = [] # client socket 목록
rooms = {} # 채팅방 목록

def readUserFile():
    try:
        with open("onlineUsers.txt", 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."

def updateUsers():
    for clientSocket in clients:
        userList = "\n\n<현재 접속 중인 User List>\n" + readUserFile()
        clientSocket.send(userList.encode())

def writeUserFile():
    with open("onlineUsers.txt", 'w') as f:
        for nickname, (ip, port, _) in users.items():
            user_data = f"Id: {nickname}\nIP: {ip}\nPort: {port}\n"
            f.write(user_data + '\n')

def handleClient(clientSocket, client_address):
    ip, port = client_address
    print(f"클라이언트 {ip}:{port} 연결")

    nickname = ""
    while True:
        clientSocket.send("닉네임을 입력하세요: ".encode())
        nickname = clientSocket.recv(1024).decode().strip()
        if nickname in users:
            clientSocket.send("이미 사용 중인 닉네임입니다. 다른 닉네임을 입력하세요: ".encode())
        elif not nickname:
            clientSocket.send("올바른 닉네임을 입력해주세요.".encode())
        else:
            clientSocket.send(f"환영합니다. {nickname}님".encode())
            break 

    users[nickname] = [ip, port, clientSocket]
    writeUserFile()
    updateUsers()
    clients.append(clientSocket) # 사용자 socket 저장
    userList = "<현재 접속 중인 User List>\n" + readUserFile()
    clientSocket.send(userList.encode())

    while True: # 명령어 검사 및 기능
        try:
            data = clientSocket.recv(1024).decode().strip()
            if not data:
                break

            if data.startswith('/sendR'):
                _, roomName, c_msg = data.split(' ', 2)
                if roomName in rooms:
                    for client in rooms[roomName]:
                        client.send(f"\n{nickname}: {c_msg}".encode())
                else:
                    clientSocket.send(f"{roomName}을 찾을 수 없습니다.".encode())
            
            elif data.startswith('/create'):
                _, roomName = data.split(' ', 1)
                if roomName not in rooms:
                    rooms[roomName] = [users[nickname][2]]
                    clientSocket.send(f"\"{roomName}\"을 만들었습니다.".encode())
                else:
                    clientSocket.send(f"{roomName}이 이미 존재합니다.".encode())
                
            elif data.startswith('/invite'):
                _, userName, roomName = data.split(' ')
                if roomName in rooms:
                    if userName in users:
                        if users[userName][2] not in rooms[roomName]:
                            rooms[roomName].append(users[userName][2])
                            users[userName][2].send(f"{nickname}님이 당신을 {roomName}에 초대했습니다.".encode())
                            clientSocket.send(f"{userName}을 {roomName}에 초대했습니다.".encode())
                        else:
                            clientSocket.send(f"{userName}가 {roomName}에 이미 존재합니다.".encode())
                    else:
                        clientSocket.send(f"사용자 {userName}를 찾을 수 없습니다.".encode())
                else:
                    clientSocket.send(f"{roomName}을 찾을 수 없습니다.".encode())
                
            elif data.startswith('/send'):
                _, userName, c_msg = data.split(' ', 2)
                if userName in users:
                    clientSocket.send(f"\n{nickname}: {c_msg}".encode())
                    users[userName][2].send(f"\n{nickname}: {c_msg}".encode())
                else:
                    clientSocket.send(f"사용자 {userName}를 찾을 수 없습니다.".encode())

            elif data.startswith('/del'):
                _, roomName = data.split(' ', 1)
                if roomName in rooms:
                    del rooms[roomName]
                    clientSocket.send(f"\"{roomName}\"을 삭제했습니다.".encode())
                else:
                    clientSocket.send(f"{roomName}을 찾을 수 없습니다.".encode())

            elif data == '/roomlist':
                clientSocket.send(f"{rooms}".encode())
            
            elif data == '/exit':
                clientSocket.send(f"메신저가 종료됩니다.".encode())
                if nickname in users: # 사용자 삭제
                    del users[nickname]
                    writeUserFile()
                    updateUsers()
                    break
            
            else:
                clientSocket.send("명령어를 다시 입력 해주세요.".encode())

        except Exception as e:
            print(f"Error in {nickname}: {e}")
            break

    

if __name__ == "__main__":
    HOST = "localhost"
    PORT = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    print("서버 실행")

    while True:
        clientSocket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handleClient, args=(clientSocket, client_address))
        client_thread.start()
