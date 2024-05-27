import socketserver

class ServerHandler(socketserver.BaseRequestHandler):
    # 접속 유저 관리
    users = {}

    def readUserFile(self):
        try:
            with open("onlineUsers.txt", 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
    
    def writeUserFile(self):
        with open("onlineUsers.txt", 'w') as f:
            for nickname, (ip, port) in self.users.items():
                userData = f"Id: {nickname}\nIP: {ip}\nPort: {port}"
                f.write(userData + '\n\n')
    
    def handle(self):
        ip, port = self.client_address
        print("클라이언트 연결")

        self.request.send("닉네임을 입력하세요".encode())
        nickname = self.request.recv(1024).decode().strip()
        if not nickname:
            self.request.close()
            return

        while nickname in self.users:
            self.request.send("이미 사용 중인 닉네임입니다. 다른 닉네임을 입력하세요: ".encode())
            nickname = self.request.recv(1024).decode().strip()
            if not nickname:
                self.request.close()
                return

        self.users[nickname] = (ip, port)
        self.writeUserFile()  # 새로운 사용자가 추가되면 파일에 새로 쓰기
        userList = "< 현재 접속 중인 User List >\n" + self.readUserFile()
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
    chat = ChatServer(("", 8000), ServerHandler)
    chat.serve_forever()
