# -*- encoding: utf-8 -*-
'''
@File         :T2.py
@Time         :2020/07/12 00:35:14
@Author       :kevenano
@Description  :双链表实现无序表
@Version      :1.0
'''


class Node:
    def __init__(self, prev=None, item=None, Next=None):
        self.prev = prev
        self.item = item
        self.next = Next


class unOrderedList:
    """单链表实现无序表"""

    def __init__(self):
        """初始化"""
        self.head = Node()
        self.rear = Node()
        self.head.next = self.rear
        self.rear.prev = self.head
        self.size = 0

    def __len__(self):
        """
        链表长度
        不建议使用
        考虑 unOrderedList.size
        """
        itemCnt = 0
        tmpNode = self.head.next
        while tmpNode.next is not None:
            itemCnt += 1
        return itemCnt

    def __repr__(self):
        """
        print(unOrderedList)
        """
        itemStr = ""
        curNode = self.head.next
        while curNode.next is not None:
            itemStr = itemStr + str(curNode.item) + " "
            curNode = curNode.next
        return itemStr

    def isEmpty(self) -> bool:
        """是否为空链"""
        return self.size == 0

    def add(self, item):
        """向表头添加元素"""
        newNode = Node(self.head, item, self.head.next)
        self.head.next.prev = newNode
        self.head.next = newNode
        self.size += 1

    def remove(self, item) -> int:
        """
        移除元素
        元素存在并成功移除返回 1
        元素不存在返回 -1
        """
        if self.isEmpty():
            raise Exception("List is empty!")
        # preNode = self.head
        curNode = self.head.next
        while curNode.item != item:
            if curNode.next.next is None:
                return -1
            # preNode = curNode
            curNode = curNode.next
        curNode.prev.next = curNode.next
        curNode.next.prev = curNode.prev
        # del curNode
        self.size -= 1
        return 1

    def exist(self, item) -> bool:
        """元素是否存在"""
        return self.getIndex(item) is not None

    def getIndex(self, item):
        """
        获取item第一次出现的索引值
        若item不存在，返回None
        """
        if self.isEmpty():
            raise Exception("List is empty!")
        tmpNode = self.head.next
        index = 0
        while tmpNode.item != item:
            if tmpNode.next.next is None:
                return None
            tmpNode = tmpNode.next
            index += 1
        return index

    def getItem(self, index):
        """根据索引获取元素"""
        if self.isEmpty():
            raise Exception("List is empty!")
        if index >= self.size:
            raise IndexError("Index out of range!")
        if index <= self.size//2:
            curInd = 0
            curNode = self.head.next
            while curInd != index:
                if curNode.next.next is None:
                    return None
                curNode = curNode.next
                curInd += 1
            return curNode.item
        else:
            curInd = self.size - 1
            curNode = self.rear.prev
            while curInd != index:
                if curNode.prev.prev is None:
                    return None
                curNode = curNode.prev
                curInd -= 1
            return curNode.item

    def append(self, item):
        """向表尾添加元素"""
        newNode = Node(self.rear.prev, item, self.rear)
        self.rear.prev.next = newNode
        self.rear.prev = newNode
        self.size += 1

    def insert(self, index, item):
        """插入元素"""
        if index >= self.size:
            raise IndexError("Index out of range!")
        if index <= self.size//2:
            curInd = 0
            curNode = self.head
            while curInd != index:
                curInd += 1
                curNode = curNode.next
            newNode = Node(curNode, item, curNode.next)
            curNode.next.prev = newNode
            curNode.next = newNode
            self.size += 1
        else:
            curInd = self.size - 1
            curNode = self.rear.prev
            while curInd != index:
                curInd -= 1
                curNode = curNode.prev
            newNode = Node(curNode.prev, item, curNode)
            curNode.prev.next = newNode
            curNode.prev = newNode
            self.size += 1

    def pop(self, index=None):
        """抛出元素"""
        if self.isEmpty():
            raise Exception("List is empty!")
        if index is not None and index >= self.size:
            raise IndexError("Index out of range!")
        if index is None:
            # preNode = self.head
            curNode = self.rear.prev
            self.rear.prev = curNode.prev
            curNode.prev.next = self.rear
            # del curNode
            self.size -= 1
            return curNode.item
        else:
            if index <= self.size//2:
                curInd = 0
                # preNode = self.head
                curNode = self.head.next
                while curInd != index:
                    # preNode = curNode
                    curNode = curNode.next
                    curInd += 1
                # curNode.prev.next = curNode.next
                # curNode.next.prev = curNode.prev
                # # del curNode
                # self.size -= 1
                # return curNode.item
            else:
                curInd = self.size - 1
                curNode = self.rear.prev
                while curInd != index:
                    curInd -= 1
                    curNode = curNode.prev
            curNode.prev.next = curNode.next
            curNode.next.prev = curNode.prev
            # del curNode
            self.size -= 1
            return curNode.item


def test():
    testList = unOrderedList()
    for i in range(10):
        testList.add(i)
    # testList.remove(0)
    print(testList)


if __name__ == "__main__":
    test()