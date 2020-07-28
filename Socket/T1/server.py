# -*- encoding: utf-8 -*-
'''
@File         :server.py
@Time         :2020/07/25 20:36:08
@Author       :kevenano
@Description  :网络编程1：服务器端
@Version      :1.0
'''

import socket
import threading
import time


class Solution():
    def __init__(self, ip: str, porto: int):
        # 创建套接字
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        # 绑定服务器监听端口
        self.socket.bind((ip, porto))
    
    def start(self):
        self.socket.listen(5)
        print("Waiting for connection...")
        while True:
            sock, addr = self.socket.accept()
            t = threading.Thread(target=self.tcplink, args=(sock, addr))
            t.start()
    
    def tcplink(self, sock: socket.socket, addr: tuple):
        print("Accept new connection from %s:%s..." % addr)
        sock.send(b"Welcome!")
        while True:
            data = sock.recv(1024)
            time.sleep(1)
            if not data or data.decode("utf-8") == "exit":
                break
            sock.send(("Hello, %s" % data.decode("utf-8")).encode("utf-8"))
        sock.close()
        print("Connection from %s:%s closed." % addr)


def main():
    S = Solution("127.0.0.1", 9999)
    S.start()


if __name__ == "__main__":
    main()
