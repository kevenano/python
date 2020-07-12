# -*- encoding: utf-8 -*-
"""
@File         :T1.py
@Time         :2020/07/11 21:44:46
@Author       :kevenano
@Description  :用单链表实现无序表
@Version      :1.0
"""


class Node:
    def __init__(self, item=None, Next=None):
        self.item = item
        self.next = Next


class unOrderedList:
    """单链表实现无序表"""

    def __init__(self):
        """初始化"""
        self.head = Node()
        self.size = 0

    def __len__(self):
        """
        链表长度
        不建议使用
        考虑 unOrderedList.size
        """
        itemCnt = 0
        tmpNode = self.head.next
        while tmpNode is not None:
            itemCnt += 1
            tmpNode = tmpNode.next
        return itemCnt

    def __repr__(self):
        """
        print(unOrderedList)
        """
        itemStr = ""
        curNode = self.head.next
        while curNode is not None:
            itemStr = itemStr + str(curNode.item) + " "
            curNode = curNode.next
        return itemStr

    def isEmpty(self) -> bool:
        """是否为空链"""
        return self.head.next is None

    def add(self, item):
        """向表头添加元素"""
        tmpNode = Node(item, self.head.next)
        self.head.next = tmpNode
        self.size += 1

    def remove(self, item) -> int:
        """
        移除元素
        元素存在并成功移除返回 1
        元素不存在返回 -1
        """
        if self.isEmpty():
            raise Exception("List is empty!")
        preNode = self.head
        curNode = preNode.next
        while curNode.item != item:
            if curNode.next is None:
                return -1
            preNode = curNode
            curNode = curNode.next
        preNode.next = curNode.next
        del curNode
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
            if tmpNode.next is None:
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
        curInd = 0
        curNode = self.head.next
        while curInd != index:
            if curNode.next is None:
                return None
            curNode = curNode.next
            curInd += 1
        return curNode.item

    def append(self, item):
        """向表尾添加元素"""
        tmpNode = self.head.next
        while tmpNode.item is not None:
            tmpNode = tmpNode.next
        tmpNode.next = Node(item)
        self.size += 1

    def insert(self, index, item):
        """插入元素"""
        if index >= self.size:
            raise IndexError("Index out of range!")
        curInd = 0
        curNode = self.head
        while curInd != index:
            curInd += 1
            curNode = curNode.next
        newNode = Node(item, curNode.next)
        curNode.next = newNode
        self.size += 1

    def pop(self, index=None):
        """抛出元素"""
        if self.isEmpty():
            raise Exception("List is empty!")
        if index is not None and index >= self.size:
            raise IndexError("Index out of range!")
        if index is None:
            preNode = self.head
            curNode = preNode.next
            while curNode.next is not None:
                preNode = curNode
                curNode = curNode.next
            preNode.next = None
            # del curNode
            self.size -= 1
            return curNode.item
        else:
            curInd = 0
            preNode = self.head
            curNode = preNode.next
            while curInd != index:
                preNode = curNode
                curNode = curNode.next
                curInd += 1
            preNode.next = curNode.next
            # del curNode
            self.size -= 1
            return curNode.item


def test():
    testList = unOrderedList()
    for i in range(10):
        testList.add(i)
    print(testList)


if __name__ == "__main__":
    test()
