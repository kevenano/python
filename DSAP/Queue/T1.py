# -*- encoding: utf-8 -*-
"""
@File         :T1.py
@Time         :2020/07/11 00:43:48
@Author       :kevenano
@Description  :队列的应用：热土豆问题
@Version      :1.0
"""

from CLASS_QUEUE import Queue
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Solution:
    def hotPotato(self, nameList, num):
        """
        nameList: 人名列表
        num: 传土豆次数
        """
        resQueue = Queue()
        for item in nameList:
            resQueue.enqueue(item)
        while len(resQueue) > 1:
            for cnt in range(num):
                resQueue.enqueue(resQueue.dequeue())
            resQueue.dequeue()
        return resQueue.first()


def main():
    so = Solution()
    nameCnt = list(range(10, 11))
    testNum = list(range(2, 100))
    res = np.zeros(shape=[len(nameCnt), len(testNum)], dtype=int)
    for cnt in nameCnt:
        for num in testNum:
            res[cnt-nameCnt[0]][num-testNum[0]] = so.hotPotato(list(range(1, cnt+1)), num)
    # 绘图
    fig = plt.figure()
    ax1 = Axes3D(fig)
    # ax2 = Axes3D(fig)
    X, Y = np.meshgrid(nameCnt, testNum)
    ax1.scatter(X, Y, res)
    # ax2.plot_surface(X, Y, res)
    plt.show()


if __name__ == "__main__":
    main()
