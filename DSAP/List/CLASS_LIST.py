# -*- encoding: utf-8 -*-
"""
@File         :CLASS_LIST.py
@Time         :2020/07/12 15:26:46
@Author       :kevenano
@Description  :ADT线性表
@Version      :1.0
"""


# 单向节点
class _Node:
    """单向节点"""

    def __init__(self, item=None, Next=None):
        self.item = item
        self.next = Next


# 双向节点
class _DuLNode(_Node):
    """双向节点"""

    def __init__(self, Prev=None, item=None, Next=None):
        super().__init__(item, Next)
        self.prev = Prev


# 单链表实现无序表
class SLunOrderedList:
    """单链表实现无序表"""

    def __init__(self):
        """初始化"""
        self.head = _Node()
        self.size = 0

    def __len__(self):
        """
        链表长度
        不建议使用
        考虑 List.size
        """
        itemCnt = 0
        tmpNode = self.head.next
        while tmpNode is not None:
            itemCnt += 1
            tmpNode = tmpNode.next
        return itemCnt

    def __repr__(self):
        """
        print(List)
        """
        itemStr = ""
        curNode = self.head.next
        while curNode is not None:
            itemStr = itemStr + str(curNode.item) + " "
            curNode = curNode.next
        return itemStr

    def isEmpty(self) -> bool:
        """是否为空"""
        return self.head.next is None

    def add(self, item):
        """向表头添加元素"""
        tmpNode = _Node(item, self.head.next)
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
        tmpNode.next = _Node(item)
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
        newNode = _Node(item, curNode.next)
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


# 双链表实现无序表
class DLunOrderedList:
    """双链表实现无序表"""

    def __init__(self):
        """初始化"""
        self.head = _DuLNode()
        self.rear = _DuLNode()
        self.head.next = self.rear
        self.rear.prev = self.head
        self.size = 0

    def __len__(self):
        """
        链表长度
        不建议使用
        考虑 List.size
        """
        itemCnt = 0
        tmpNode = self.head.next
        while tmpNode.next is not None:
            itemCnt += 1
            tmpNode = tmpNode.next
        return itemCnt

    def __repr__(self):
        """
        print(List)
        """
        itemStr = ""
        curNode = self.head.next
        while curNode.next is not None:
            itemStr = itemStr + str(curNode.item) + " "
            curNode = curNode.next
        return itemStr

    def isEmpty(self) -> bool:
        """是否为空"""
        return self.size == 0

    def add(self, item):
        """向表头添加元素"""
        newNode = _DuLNode(self.head, item, self.head.next)
        self.head.next.prev = newNode
        self.head.next = newNode
        self.size += 1

    def remove(self, item, direction="forward") -> int:
        """
        移除元素
        direction="forward" 从前往后插
        direction="reverse" 从后往前插
        return  1 元素存在并成功移除
        return -1 元素不存在
        """
        if direction not in ("forward", "reverse"):
            raise Exception("Parameter error!")
        if direction == "forward":
            curNode = self.head
            while curNode.item != item:
                if curNode.next.next is None:
                    return -1
                curNode = curNode.next
            curNode.prev.next = curNode.next
            curNode.next.prev = curNode.prev
            self.size -= 1
            return 1
        else:
            curNode = self.rear
            while curNode.item != item:
                if curNode.prev.prev is None:
                    return -1
                curNode = curNode.prev
            curNode.prev.next = curNode.next
            curNode.next.prev = curNode.prev
            self.size -= 1
            return 1

    def exist(self, item, direction="forward") -> bool:
        """
        元素是否存在
        direction="forward" 从前往后查找
        direction="reverse" 从后往前查找
        """
        return self.getIndex(item, direction) is not None

    def getIndex(self, item, direction="forward"):
        """
        获取item第一次出现的索引值
        direction="forward" 从前往后查找
        direction="reverse" 从后往前查找
        若item不存在，返回None
        """
        if self.isEmpty():
            raise Exception("List is empty!")
        if direction == "forward":
            tmpNode = self.head.next
            index = 0
            while tmpNode.item != item:
                if tmpNode.next.next is None:
                    return None
                tmpNode = tmpNode.next
                index += 1
            return index
        else:
            tmpNode = self.rear.prev
            index = self.size - 1
            while tmpNode.item != item:
                if tmpNode.prev.prev is None:
                    return None
                tmpNode = tmpNode.prev
                index -= 1
            return index

    def getItem(self, index):
        """根据索引获取元素"""
        if self.isEmpty():
            raise Exception("List is empty!")
        if index >= self.size:
            raise IndexError("Index out of range!")
        if index <= self.size // 2:
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
        newNode = _DuLNode(self.rear.prev, item, self.rear)
        self.rear.prev.next = newNode
        self.rear.prev = newNode
        self.size += 1

    def insert(self, index, item):
        """插入元素"""
        if index >= self.size:
            raise IndexError("Index out of range!")
        if index <= self.size // 2:
            curInd = 0
            curNode = self.head.next
            while curInd != index:
                curInd += 1
                curNode = curNode.next
        else:
            curInd = self.size - 1
            curNode = self.rear.prev
            while curInd != index:
                curInd -= 1
                curNode = curNode.prev
        newNode = _DuLNode(curNode.prev, item, curNode)
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
            if index <= self.size // 2:
                curInd = 0
                # preNode = self.head
                curNode = self.head.next
                while curInd != index:
                    # preNode = curNode
                    curNode = curNode.next
                    curInd += 1
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


# 单链表实现有序表
class SLOrderedList(SLunOrderedList):
    """单链表实现有序表"""

    def add(self, item):
        """添加元素"""
        preNode = self.head
        curNode = self.head.next
        while curNode is not None and curNode.item < item:
            preNode = curNode
            curNode = curNode.next
        newNode = _Node(item, curNode)
        preNode.next = newNode
        self.size += 1

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
            if tmpNode.next is None or tmpNode.item > item:
                return None
            tmpNode = tmpNode.next
            index += 1
        return index

    def append(self):
        raise AttributeError("'SLOrderedList' object has no attribute 'append'!")

    def insert(self):
        raise AttributeError("'SLOrderedList' object has no attribute 'insert'!")


# 双链表实现有序表
class DLOrderedList(DLunOrderedList):
    """双链表实现有序表"""

    def add(self, item, direction="forward"):
        """
        插入元素
        direction="forward" 从前往后插
        direction="reverse" 从后往前插
        """
        if direction not in ("forward", "reverse"):
            raise Exception("Parameter error!")
        if self.isEmpty():
            newNode = _DuLNode(self.head, item, self.rear)
            self.head.next = newNode
            self.rear.prev = newNode
            self.size += 1
        else:
            if direction == "forward":
                curNode = self.head.next
                while curNode.next is not None and curNode.item <= item:
                    curNode = curNode.next
                newNode = _DuLNode(curNode.prev, item, curNode)
                curNode.prev.next = newNode
                curNode.prev = newNode
                self.size += 1
            else:
                curNode = self.rear.prev
                while curNode.prev is not None and curNode.item >= item:
                    curNode = curNode.prev
                newNode = _DuLNode(curNode, item, curNode.next)
                curNode.next.prev = newNode
                curNode.next = newNode
                self.size += 1

    def getIndex(self, item, direction="forward"):
        """
        获取item第一次出现的索引值
        direction="forward" 从前往后查找
        direction="reverse" 从后往前查找
        若item不存在，返回None
        """
        if self.isEmpty():
            raise Exception("List is empty!")
        if direction == "forward":
            tmpNode = self.head.next
            index = 0
            while tmpNode.item != item:
                if tmpNode.next.next is None or tmpNode.item > item:
                    return None
                tmpNode = tmpNode.next
                index += 1
            return index
        else:
            tmpNode = self.rear.prev
            index = self.size - 1
            while tmpNode.item != item:
                if tmpNode.prev.prev is None or tmpNode.item < item:
                    return None
                tmpNode = tmpNode.prev
                index -= 1
            return index

    def append(self):
        raise AttributeError("'DLOrderedList' object has no attribute 'append'!")

    def insert(self):
        raise AttributeError("'DLOrderedList' object has no attribute 'insert'!")


"""
def test():
    listA = SLunOrderedList()
    listB = DLunOrderedList()
    listC = SLOrderedList()
    listD = DLOrderedList()

    testItem = [1, 9, 7, 2, 7, 7, 4, 6, 8, 4]
    for i in testItem:
        listA.add(i)
        listB.add(i)
        listC.add(i)
        listD.add(i, "reverse")

    print(listA)
    print(listB)
    print(listC)
    print(listD)
    print(listD)


if __name__ == "__main__":
    test()
"""
