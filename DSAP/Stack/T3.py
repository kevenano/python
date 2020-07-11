# -*- encoding: utf-8 -*-
"""
@File         :T3.py
@Time         :2020/07/06 22:18:48
@Author       :kevenano
@Description  :栈的应用：表达式转换及后缀表达式求值
@Version      :1.0
"""

from CLASS_STACK import Stack


class Solution:
    def midToRight(self, stringIn: str) -> list:
        """
        中缀转后缀
        策略：
        从左至右依次扫描，数字或变量直接加入res末尾
        若当前元素为符号:
            若符号栈为空, 压入元素
            若当前元素优先级小于等于栈顶元素：
                抛出栈顶元素直到上述条件不成立或栈顶为“（”
                将当前元素压入栈
            若上述条件不成立，压入元素
        若当前元素为“）”：
            抛出栈顶元素直到栈顶为“（”
            抛出栈顶的“（”
        其他情况（数字或变量）：
            直接加入结果末尾
        最后清空栈
        """
        symbolStack = Stack()
        symbolPriority = {"(": 5, "/": 4, "*": 3, "-": 2, "+": 1}
        itemList = stringIn.split(" ")
        res = []
        for item in itemList:
            if item == " " or item == "":
                continue
            if item in symbolPriority.keys():
                if symbolStack.isEmpty():
                    symbolStack.push(item)
                elif symbolPriority[item] <= symbolPriority[symbolStack.peek()]:
                    while (
                        symbolStack.isEmpty() is False
                        and symbolPriority[item] <= symbolPriority[symbolStack.peek()]
                        and symbolStack.peek() != "("
                    ):
                        res.append(symbolStack.pop())
                    symbolStack.push(item)
                else:
                    symbolStack.push(item)
            elif item == ")":
                while symbolStack.peek() != "(":
                    res.append(symbolStack.pop())
                symbolStack.pop()
            else:
                res.append(item)
        while symbolStack.isEmpty() is False:
            res.append(symbolStack.pop())
        return res

    def calRight(self, listIn):
        S = Stack()
        for item in listIn:
            if item not in "+-*/":
                S.push(float(item))
            else:
                op2 = S.pop()
                op1 = S.pop()
                if item == "+":
                    S.push(op1+op2)
                if item == "-":
                    S.push(op1-op2)
                if item == "*":
                    S.push(op1*op2)
                if item == "/":
                    S.push(op1/op2)
        return S.pop()


def main():
    so = Solution()
    testString = "8 * 3 + ( 2 + 3 * 5 - 3 * 2 + 2 - 1 ) * 5 + 3 - ( 6 / ( 2 + 1 * 3 ) )"
    testList = so.midToRight(testString)
    testCal = so.calRight(testList)
    print(testList)
    print(testCal)


if __name__ == "__main__":
    main()
