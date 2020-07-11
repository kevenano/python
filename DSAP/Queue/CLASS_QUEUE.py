# -*- encoding: utf-8 -*-
'''
@File         :CLASS_QUEUE.py
@Time         :2020/07/11 00:08:55
@Author       :kevenano
@Description  :队列Queue
@Version      :1.0
'''


class Queue():
    """列表实现队列，第一个元素为队尾"""
    def __init__(self):
        """初始化一个空队列"""
        self.data = []

    def __len__(self):
        """队列长度"""
        return len(self.data)

    def isEmpty(self):
        """队列是否为空"""
        return len(self.data) == 0

    def first(self):
        """查看队首元素"""
        if self.isEmpty():
            raise Exception("Queue is empty!")
        return self.data[-1]

    def enqueue(self, item):
        """向队尾插入元素"""
        self.data.insert(0, item)

    def dequeue(self):
        """队首元素出队"""
        if self.isEmpty():
            raise Exception("Queue is empty!")
        return self.data.pop()
