import socketserver

class ServerHandler(socketserver.BaseRequestHandler):
    # 접속 유저 관리
    users = {}
    clients = []

    def readUserFile(self):
        try:
            with open("onlineUsers.txt", 'r') as f:
                return f.read()
        except FileNotFoundError:
            return "파일을 찾을 수 없습니다."
    
    def updateUsers(self):
        for i in self.clients:
            userList = "\n\n                                                                                                                                                                                                                                                                                                          <현재 접속 중인 User List>\n" + self.readUserFile()
            i.send(userList.encode())
        
    def writeUserFile(self):
        with open("onlineUsers.txt", 'w') as f:
            for nickname, (ip, port) in self.users.items():
                userData = f"Id: {nickname}\nIP: {ip}\nPort: {port}\n"
                f.write(userData + '\n')
    
    def handle(self):
        ip, port = self.client_address
        print("클라이언트 연결")
        nickname = "" 
              
        while True:
            self.request.send("닉네임을 입력하세요".encode())
            nickname = self.request.recv(1024).decode().strip()
            if nickname in self.users:
                self.request.send("이미 사용 중인 닉네임입니다. 다른 닉네임을 입력하세요: ".encode())
            elif not nickname:
                self.request.send("올바른 닉네임을 입력해주세요.".encode())
            else:
                self.request.send(f"환영합니다. {nickname}님".encode())
                break 
            
        self.users[nickname] = (ip, port)
        self.writeUserFile()  # 새로운 사용자가 추가되면 파일에 새로 쓰기
        self.updateUsers()
        self.clients.append(self.request) # 사용자 socket저장
        userList = "<현재 접속 중인 User List>\n" + self.readUserFile()
        self.request.send(userList.encode())

        while True:
            try:
                data = self.request.recv(1024).decode().strip()
                if not data:
                    break
            except ConnectionResetError:
                break

        if nickname in self.users:
            del self.users[nickname]
            self.writeUserFile()  # 사용자가 나가면 파일에서 삭제

class ChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    print("서버 실행")
    chat = ChatServer(("", 8001), ServerHandler)
    chat.serve_forever()
    chat.server_close()
