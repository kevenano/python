# -*- encoding: utf-8 -*-
"""
@File         :T2.py
@Time         :2020/07/11 11:17:49
@Author       :kevenano
@Description  :队列的应用：打印系统模拟
@Version      :1.0
"""

from CLASS_QUEUE import Queue
from random import randint


class Solution:
    def __init__(self, ppm: int, workDis: dict, pageDis: dict):
        """
        ppm：打印速度 单位：页/分钟
        workDis: 每小时任务总数概率分布字典
        pageDis: 每件任务总页数概率分布字典
        """
        self.Printer = Printer(ppm)
        self.workDis = workDis
        self.pageDis = pageDis

    def simulate(self, totalTime: int):
        """
        模拟运行打印机
        totalTime: 模拟运行总时间 单位：秒
        return: (平均等待时间，剩余任务数量)
        """
        self.Printer.clear()
        workQueue = Queue()
        waitTIme = []
        workNum = 0
        for curTick in range(totalTime):
            if randint(1, 3600) in range(1, randKey(self.workDis) + 1):
                workPage = randKey(self.pageDis)
                # print(workPage, curTick)
                workQueue.enqueue(workPage)
                waitTIme.append(curTick)
            if not workQueue.isEmpty() and self.Printer.isFree():
                waitTIme[workNum] = curTick - waitTIme[workNum]
                workNum += 1
                self.Printer.newTask(workQueue.dequeue())
            self.Printer.tick()
        return sum(waitTIme) // len(waitTIme), len(workQueue)


# 打印机
class Printer:
    def __init__(self, ppm: int):
        self.ppm = ppm
        self.resTime = 0

    def clear(self):
        self.resTime = 0

    def newTask(self, pageNum):
        if self.isFree() is False:
            raise Exception("Printer is now bussy!")
        self.resTime = int(pageNum * 60 / self.ppm)

    def isFree(self):
        return self.resTime == 0

    def tick(self):
        if self.resTime >= 1:
            self.resTime -= 1
        else:
            self.resTime = 0


def randKey(proDis: dict) -> int:
    """
    根据概率分布列表返回随机Key
    """
    start = 0
    randNum = randint(1, sum(proDis.values()))
    for k, v in proDis.items():
        start += v
        if randNum <= start:
            break
    return k


def main():
    workDis = {5: 5, 10: 8, 15: 10, 20: 3, 25: 2}
    pageDis = {5: 3, 8: 4, 10: 15, 15: 6, 20: 2, 25: 2}
    so = Solution(ppm=10, workDis=workDis, pageDis=pageDis, totalTime=3600)
    waitTimeCnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    wts = 0
    rns = 0
    for i in range(1000):
        print(i)
        wt, rn = so.simulate()
        wts += wt
        rns += rn
        try:
            waitTimeCnt[wt // 30] += 1
        except IndexError:
            waitTimeCnt[-1] += 1
    print(waitTimeCnt)
    print(wts/(i+1), rns/(i+1))


if __name__ == "__main__":
    main()
