# 新思路 直接爬取数据库 本地处理下载文件部分IDA 
# 实质：从网站爬取文件的静态URL 使用多线程下载工具下载
# 减轻代码负担
# but 如果网站数据库更新，链接更新，本地数据库也必须更新
# 缺点：对于拥有动态链接的资源本方法不适用（如e站资源）
import requests
import os
import time
import threading
import my_fake_useragent as mfua
from random import randint

lock = threading.Lock()


# 记录时间 创建工作目录
startTime = time.time()
taskId = int(startTime)
taskPath = os.path.join(os.getcwd(), str(taskId))
os.mkdir(taskPath)
jsonPath = os.path.join(taskPath, "json")
os.mkdir(jsonPath)

# 初始化错误列表
failedList = []


# Html download function
# 输入参数reFlag = 0 返回text, 1 返回content, 2 返回resp
# 若下载失败， 一律返回None
def download(
    url, num_retries=3, headers={}, cookie="", params="", reFlag=0, timeout=(30, 300),
):
    # print("Downloading: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = mfua.UserAgent().random()
    if cookie != "":
        headers["cookie"] = cookie
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
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
        resp = None
    if reFlag == 0:
        return html
    elif reFlag == 1:
        return content
    else:
        return resp


# 多线程下载保存json
def downJson(url, urlParams):
    global failedList
    global jsonPath
    # 打印提示信息
    if lock.acquire():
        print("Deal with page ", urlParams["page"])
        print()
        lock.release()
    # 尝试下载json
    res = download(url=url, params=urlParams, reFlag=2, timeout=(30, 60))
    if (res is None or len(res.content) < 1000) and lock.acquire():
        # 更新错误列表
        failedList.append(urlParams["page"])
        lock.release()
        print(f"Page {urlParams['page']} fail...")
        print()
    else:
        # 保存json
        tmpPath = os.path.join(jsonPath, str(urlParams["page"]) + ".json")
        pageFile = open(tmpPath, "w", encoding="utf-8")
        pageFile.write(res.text)
        pageFile.close()
        del tmpPath


def writeLog(startPage, endPage, CNT):
    global startTime
    global taskId
    global taskPath
    global jsonPath
    logPath = os.path.join(taskPath, f"log_{str(CNT)}.txt")
    failedList

    endTime = time.time()
    spendTime = int(endTime - startTime)
    logFile = open(logPath, "w")
    logFile.write("Task ID:\n")
    logFile.write(str(taskId) + "\n")
    logFile.write("Pages:\n")
    logFile.write(str(startPage) + "-" + str(endPage) + "\n")
    logFile.write("Failed Count:\n")
    logFile.write(str(len(failedList)) + "\n")
    logFile.write("Failed List:\n")
    logFile.write(str(failedList).replace(",", "\n") + "\n")
    logFile.write("Start Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) + "\n")
    logFile.write("End Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime)) + "\n")
    logFile.write("Time Cost:\n")
    logFile.write(str(spendTime // 3600) + "h")
    logFile.write(str((spendTime % 3600) // 60) + "m")
    logFile.write(str(spendTime % 60) + "s" + "\n")
    logFile.write("\n\n\n\n\nOriginal Failed List:\n")
    logFile.write(str(failedList))
    logFile.close()


# 获取参数
def getParams():
    flag = 0
    flag = int(input("Range or List? 0 for Range, 1 for List :\n"))
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
        startPage = int(input("Start Page:\n"))
        endPage = int(input("End Page:\n"))
        if startPage < 1:
            startPage = 1
        if endPage < startPage:
            endPage = startPage
        pageList = list(range(startPage, endPage))
    limit = int(input("Limit:\n"))
    if limit < 21:
        limit = 21
    if limit > 100:
        limit = 100
    threadNum = int(input("Thread Number:\n"))
    if threadNum < 1:
        threadNum = 1
    if threadNum > 20:
        threadNum = 20

    return pageList, limit, threadNum


# 主函数
def main():
    # 获取参数
    pageList, limit, threadNum = getParams()
    # 初始化相关参数
    pageCnt = 0  # 完成的任务数
    cnt = 0
    url = "https://konachan.com/post.json"
    params = {"limit": limit, "tags": "order:id", "page": pageList[0]}

    # 循环获取所有指定页面
    while pageCnt < len(pageList):
        # 创建多线程任务
        if threadNum > len(pageList) - pageCnt:
            threadNum = len(pageList) - pageCnt
        thList = []
        for i in range(threadNum):
            params["page"] = pageList[pageCnt]
            dlThread = threading.Thread(target=downJson, args=(url, params.copy()))
            thList.append(dlThread)
            dlThread.start()
            time.sleep(1)
            pageCnt += 1
        # 等待线程结束
        for thread in thList:
            thread.join()
        # 写日志
        if pageCnt % (threadNum * 10) == 0:
            writeLog(pageList[pageCnt - threadNum * 10 + 1], pageList[pageCnt], cnt)
            cnt += 1
            time.sleep(randint(60, 120))

    # 写日志
    writeLog(pageList[0], pageList[-1], cnt)

    # over!
    print("All finish!")


if __name__ == "__main__":
    main()
