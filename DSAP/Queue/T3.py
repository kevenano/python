# -*- encoding: utf-8 -*-
"""
@File         :T3.py
@Time         :2020/07/11 21:09:30
@Author       :kevenano
@Description  :队列的应用：双端队列，回文词
@Version      :1.0
"""


class Solution:
    def isPalindrome(self, inString: str) -> bool:
        if len(inString) < 2:
            raise Exception("Wrong input!")
        strDeque = Deque()
        for item in inString:
            strDeque.addFront(item)
        while len(strDeque) > 1:
            if strDeque.rmFront() != strDeque.rmRear():
                return False
        return True


# 双端队列
class Deque:
    """双端队列，列表实现，0为队尾，-1为队首"""

    def __init__(self):
        """初始化空队列"""
        self.data = []

    def __len__(self):
        """队列长度"""
        return len(self.data)

    def isEmpty(self):
        """队列是否为空"""
        return len(self.data) == 0

    def front(self):
        """队首元素"""
        if self.isEmpty():
            raise Exception("Deque is empty!")
        return self.data[-1]

    def rear(self):
        """队尾元素"""
        if self.isEmpty():
            raise Exception("Deque is empty!")
        return self.data[0]

    def addFront(self, item):
        """向队首添加元素"""
        self.data.append(item)

    def addRear(self, item):
        """向队尾添加元素"""
        self.data.insert(0, item)

    def rmFront(self):
        """队首元素出队"""
        if self.isEmpty():
            raise Exception("Deque is empty!")
        return self.data.pop()

    def rmRear(self):
        """队尾元素出队"""
        if self.isEmpty():
            raise Exception("Deque is empty!")
        return self.data.pop(0)


def main():
    so = Solution()
    testString = "kevenanonanevek"
    print(so.isPalindrome(testString))


if __name__ == "__main__":
    main()
