# -*- encoding: utf-8 -*-
'''
@File         :client.py
@Time         :2020/07/25 21:12:42
@Author       :kevenano
@Description  :网络编程1：客户端
@Version      :1.0
'''

import socket


class Solution():
    def __init__(self, ip: str, porto: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.socket.connect((ip, porto))
        print(self.socket.recv(1024).decode("utf-8"))

    def start(self):
        for data in [b'Alpha', b'Beta', b'Carol']:
            self.socket.send(data)
            print(self.socket.recv(1024).decode("utf-8"))
        self.socket.send(b"exit")
        self.socket.close()


def main():
    S = Solution("127.0.0.1", 9999)
    S.start()


if __name__ == "__main__":
    main()
