# -*- encoding: utf-8 -*-
"""
@File         :T1.py
@Time         :2020/07/06 16:43:19
@Author       :kevenano
@Description  :栈的应用：多类型括号混合匹配
@Version      :1.0
"""

from CLASS_STACK import Stack


class Solution:
    def isRightString(self, string: str) -> bool:
        S = Stack()
        opener = "([{"
        closer = ")]}"
        for item in string:
            if item in opener:
                S.push(item)
            if item in closer:
                if S.isEmpty():
                    return False
                if self._isMatch(S.peek(), item):
                    S.pop()
                else:
                    return False
        return S.isEmpty()

    def _isMatch(self, opener: str, closer: str):
        return "([{".find(opener) == ")]}".find(closer)


def main():
    testString = "((()))(a{s(fsag[f]a,[sd]346,4{(1)2}(y45)ssss,gdt(ete),[63(53)7,{g(fa),[t],{gag},[yu]}fsef])})"
    SLT = Solution()
    print(SLT.isRightString(testString))


if __name__ == "__main__":
    main()
