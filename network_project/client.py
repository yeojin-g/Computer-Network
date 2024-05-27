import socket
from threading import Thread

def recvMsg(sock):
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

# 서버에 로그인
def login_to_server(server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    while True:
        msg = sock.recv(1024).decode()
        print(msg)
        if "닉네임을 입력하세요" in msg:
            nickname = input("=> ")
            sock.send(nickname.encode())  # 닉네임을 서버로 전송
            break  # 닉네임을 입력한 후에는 반복문을 빠져나옵니다.

    recv_thread = Thread(target=recvMsg, args=(sock,))
    recv_thread.daemon = True
    recv_thread.start()

    return sock

# 사용자 간 직접 통신을 위한 함수
def direct_chat_with_user(sock, users, recipient, message):
    if recipient in users:
        ip, port = users[recipient]
        # 소켓 생성
        user_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        user_sock.connect((ip, port))

        # 메시지 전송
        send_msg = f"{recipient} {message}"
        user_sock.send(send_msg.encode())
        user_sock.close()  # 전송 후 소켓 닫기
    else:
        print("목록에 없는 사용자입니다.")

if __name__ == "__main__":
    # 서버에 로그인
    sock = login_to_server("localhost", 8000)
    users = {"alina": ("127.0.0.1", 12345), "annie": ("127.0.0.1", 12346)}  # 사용자 목록을 담을 딕셔너리

    while True:
        command = input("명령어를 입력하세요: ")
        if command.startswith("/send"):
            _, recipient, message = command.split(" ", 2)
            direct_chat_with_user(sock, users, recipient, message)
        elif command == "/exit":
            break
        else:
            print("잘못된 명령입니다.")
