# -*- encoding: utf-8 -*-
"""
@File         :T2.py
@Time         :2020/07/06 17:38:15
@Author       :kevenano
@Description  :栈的应用：进制转换
@Version      :1.0
"""

from CLASS_STACK import Stack


class Solution:
    def __init__(self):
        self.charSet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.maxBase = len(self.charSet)
        self.minBase = 2

    def decToBase(self, decIn: int, base: int) -> str:
        if decIn < 1 or base < self.minBase or base > self.maxBase:
            raise Exception("Wrong input!")
        S = Stack()
        stringOut = ""
        while decIn > 0:
            S.push(self.charSet[decIn % base])
            decIn = decIn // base
        while S.isEmpty() is False:
            stringOut = stringOut + S.pop()
        return stringOut

    def baseToDec(self, stringIn: str, base: int) -> int:
        cnt = len(stringIn) - 1
        res = 0
        for item in stringIn:
            if base > self.maxBase or item not in self.charSet or item > self.charSet[base-1]:
                raise Exception("Wrong input!")
            res = res + self.charSet.find(item)*(base**cnt)
            cnt -= 1
        return res


def main():
    so = Solution()
    testDec = 6469693230
    for testBase in range(2, 37):
        print(so.decToBase(testDec, testBase))
    print(so.baseToDec("qhm2012".upper(), 36))


if __name__ == "__main__":
    main()
