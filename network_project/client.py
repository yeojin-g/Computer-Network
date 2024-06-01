import socket
from threading import Thread
import time
import socketserver

class clientServerHandler(socketserver.BaseRequestHandler):
    def handle(self):
        pass
    
class clientChatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass



def recvMsg(sock, users):
    while True:
        try:
            msg = sock.recv(1024).decode()
            if msg:
                print(msg)
                if msg.startswith("<현재 접속 중인 User List>"):
                    parse_user_list(msg, users)
            else:
                break
        except:
            break

def parse_user_list(msg, users):
    lines = msg.split('\n')[1:]  # 첫 번째 라인은 "<현재 접속 중인 User List>"이므로 제외
    for line in lines:
        if line.startswith("Id:"):
            nickname = line.split(": ")[1]
        elif line.startswith("IP:"):
            ip = line.split(": ")[1]
        elif line.startswith("Port:"):
            port = int(line.split(": ")[1])
            users[nickname] = (ip, port)

def login_to_server(server_ip, server_port, users, clientChat):
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
    
    recv_thread = Thread(target=recvMsg, args=(sock, users))
    recv_thread.daemon = True
    recv_thread.start()
    return nickname

# 사용자 간 직접 통신을 위한 함수
def direct_chat_with_user(users, nickname, message):
    if nickname in users:
        ip, port = users[nickname]
        # 소켓 생성
        user_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user_sock.connect((ip, port))

        # 메시지 전송
        send_msg = f"{nickname}: {message}"
        user_sock.send(send_msg.encode())
        user_sock.close()  # 전송 후 소켓 닫기
    else:
        print("목록에 없는 사용자입니다.")

if __name__ == "__main__":
    # 서버에 로그인
    users = {}  # 사용자 목록을 담을 딕셔너리
    clientChat = None
    nickname = login_to_server("localhost", 8001, users, clientChat)
    time.sleep(0.5)
    
    ip, port = users[nickname]
    clientChat = clientChatServer(("localhost", port), clientServerHandler)
    clientChat.serve_forever()
    
    while True:
        command = input("명령어를 입력하세요: ")
        if command.startswith("/send"):
            _, nickname, message = command.split(" ", 2)
            direct_chat_with_user(users, nickname, message)
        elif command == "/exit":
            break
        else:
            print("잘못된 명령입니다.")

    clientChat.server_close()