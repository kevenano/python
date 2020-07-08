# -*- encoding: utf-8 -*-
'''
@File         :CLASS_STACK.py
@Time         :2020/07/06 16:37:03
@Author       :kevenano
@Description  :抽象数据类型：栈
@Version      :1.0
'''


class Stack():
    """用列表实现栈"""
    def __init__(self):
        """初始化空栈"""
        self.data = []

    def __len__(self):
        """栈的大小"""
        return len(self.data)

    def isEmpty(self):
        """栈是否为空"""
        return len(self.data) == 0

    def peek(self):
        """
        查看栈顶元素
        若为空栈，抛出错误:"Stack is empty!"
        """
        if self.isEmpty() is True:
            raise Exception("Stack is empty!")
        return self.data[-1]

    def push(self, e):
        """向栈中压入元素"""
        self.data.append(e)

    def pop(self):
        """
        移除栈顶元素
        若为空栈，抛出错误:"Stack is empty!"
        """
        if self.isEmpty() is True:
            raise Exception("Stack is empty!")
        return self.data.pop()
