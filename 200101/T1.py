# 类 测试 数字 时钟
from time import sleep


class Clock:
    hour = 0
    minutes = 0
    seconds = 0

    def __init__(self, H, M, S):
        if S >= 60:
            M += 1
            S = 0
        if M >= 60:
            H += 1
            M = 0
        if H >= 24:
            H = 0
        self.hour = H
        self.minutes = M
        self.seconds = S

    def set_time(self, H, M, S):
        if S >= 60:
            M += 1
            S = 0
        if M >= 60:
            H += 1
            M = 0
        if H >= 24:
            H = 0
        self.hour = H
        self.minutes = M
        self.seconds = S

    def run(self):
        self.seconds += 1
        self.set_time(self.hour, self.minutes, self.seconds)

    def show(self):
        print('Now is: %02d : %02d : %02d' %
              (self.hour, self.minutes, self.seconds))


def main(t):
    i = 0
    clock1 = Clock(23, 58, 56)
    while i < t:
        clock1.run()
        sleep(1)
        clock1.show()
        i += 1


if __name__ == '__main__':
    main(120)
