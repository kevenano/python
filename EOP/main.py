from random import randint
import requests
import my_fake_useragent as mfua
import time
import os
import threading
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint


lock = threading.Lock()


# 记录时间 创建工作目录
startTime = time.time()
taskId = int(startTime)
taskPath = os.path.join(os.getcwd(), str(taskId))
os.mkdir(taskPath)
htmlPath = os.path.join(taskPath, "html")
os.mkdir(htmlPath)
logPath = os.path.join(taskPath, "log.txt")


# 初始化下载错误列表和下载结束标志
indexDownFailList = []


# 通用请求头
defHeaders = {
    "Host": "www.everyonepiano.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=b280c53ee570b92e1805a9e4cbd75bad; username=kevenano; password=qhm2012%40%40%40; remember=1; huiyuan=518dSmHphWiO31f3khyj2uWo0ZYoh8AEqdZFiN0wHIURgvMyrOS5suEZLQk; FWE_getuser=kevenano; FWE_getuserid=161673; login_mima=9161d8bd2056459a0a96f80f2e6a818d; menunew=0-0-0-0; think_language=zh-CN",
    "Upgrade-Insecure-Requests": 1
}


# Html download function
# 输入参数reFlag = 0 返回text, 1 返回content, 2 返回resp
# 如下载错误，将返回resp=None
def download(
    url, num_retries=3, headers={}, cookie="", params="", reFlag=0, timeout=(30, 300),
):
    # print("Downloading: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = mfua.UserAgent().random()
    if cookie != "":
        headers["cookie"] = cookie
    resp = None
    try:
        resp = requests.get(url, headers=headers,
                            params=params, timeout=timeout)
        resp.close()
        html = resp.text
        content = resp.content
        if resp.status_code >= 400:
            print("Download error: ", resp.text)
            html = None
            content = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print("Download error!!!")
        print(e)
        html = None
        content = None
        resp = None
    except requests.exceptions.Timeout:
        print("请求超时!")
        html = None
        content = None
    if reFlag == 0:
        return html
    elif reFlag == 1:
        return content
    else:
        return resp


# 下载一页索引页
def down1index(page: int):
    global lock
    global indexDownFailList
    if page < 1:
        page = 1
    url = "https://www.everyonepiano.cn/Music.html"
    urlParams = {"p": page, "canshu": "cn_edittime", "paixu": "asc"}
    # 打印提示信息
    if lock.acquire():
        print("Deal with page ", page)
        print()
        lock.release()
    # 尝试下载
    res = download(url=url, params=urlParams, reFlag=2, timeout=(5, 10))
    if (not isinstance(res, requests.models.Response) or res.status_code != 200) and lock.acquire():
        print(f"Page {page} fail...")
        # 更新错误列表
        indexDownFailList.append(page)
        lock.release()
    else:
        # 保存html
        tmpPath = os.path.join(htmlPath, str(str(page) + ".html"))
        pageFile = open(tmpPath, "w", encoding="utf-8")
        pageFile.write(res.text)
        pageFile.close()
        del tmpPath


# 多线程下载索引页
def multiDownIndex(pageList: list, threadNum: int):
    pageCnt = 0  # 完成的任务数
    logCnt = 0
    # 循环获取所有指定页面
    while pageCnt < len(pageList):
        # 创建多线程任务
        if threadNum > len(pageList) - pageCnt:
            threadNum = len(pageList) - pageCnt
        thList = []
        for i in range(threadNum):
            page = pageList[pageCnt]
            dlThread = threading.Thread(target=down1index, kwargs={"page":page})
            thList.append(dlThread)
            dlThread.start()
            time.sleep(1)
            pageCnt += 1
        # 等待线程结束
        for thread in thList:
            thread.join()
        # 写日志 延时
        if pageCnt % (threadNum * 10) == 0:
            indexDownLog(pageList[pageCnt - threadNum * 10], pageList[pageCnt-1], logCnt)
            logCnt += 1
            print("Sleeping...")
            time.sleep(randint(30, 60))
        else:
            print("Sleeping...\n")
            time.sleep(randint(2, 5))
    indexDownLog(pageList[0], pageList[-1], logCnt)


# 获取参数
def getParams():
    pageList = []
    flag = 0
    flag = int(input("Specify Page List? 1 for Yes, 0 for No :\n"))
    if flag != 0 and flag != 1:
        print("Bye!")
        exit()
    if flag == 1:
        pageList = list(
            set(
                [
                    int(i)
                    for i in input("Input the list:\n")
                    .replace(" ", "")
                    .replace("[", "")
                    .replace("]", "")
                    .split(",")
                    if i.isdigit()
                ]
            )
        )
    else:
        startPG = int(input("Start Page:\n"))
        endPG = int(input("End Page:\n"))
        if startPG < 1:
            startPG = 1
        if endPG < startPG:
            endPG = startPG
        pageList = list(range(startPG, endPG+1))
    threadNum = int(input("Thread Number:\n"))
    if threadNum < 1:
        threadNum = 1
    if threadNum > 20:
        threadNum = 20

    return pageList, threadNum


# 写log
def indexDownLog(startPG, endPG, CNT):
    global startTime
    global taskId
    global taskPath
    global htmlPath
    global indexDownFailList
    logPath = os.path.join(taskPath, f"indexDownLog_{str(CNT)}.txt")

    endTime = time.time()
    spendTime = int(endTime - startTime)
    logFile = open(logPath, "w")
    logFile.write("Task ID:\n")
    logFile.write(str(taskId) + "\n")
    logFile.write("Page Range:\n")
    logFile.write(str(startPG) + "-" + str(endPG) + "\n")
    logFile.write("Failed Count:\n")
    logFile.write(str(len(indexDownFailList)) + "\n")
    logFile.write("Failed List:\n")
    logFile.write(str(indexDownFailList).replace(",", "\n") + "\n")
    logFile.write("Start Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) + "\n")
    logFile.write("End Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime)) + "\n")
    logFile.write("Time Cost:\n")
    logFile.write(str(spendTime // 3600) + "h")
    logFile.write(str((spendTime % 3600) // 60) + "m")
    logFile.write(str(spendTime % 60) + "s" + "\n")
    logFile.write("\n\n\n\n\nOriginal Failed List:\n")
    logFile.write(str(indexDownFailList))
    logFile.close()


# 测试
def test():
    # pageList = list(range(1, 101))
    # threadNum = 10
    pageList, threadNum = getParams()
    # pprint(pageList)
    # print(threadNum)
    multiDownIndex(pageList, threadNum)
    print("Done!")


if __name__ == "__main__":
    test()
