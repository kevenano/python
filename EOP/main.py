from random import randint
import requests
import my_fake_useragent as mfua
import time
import os
import multiprocessing
import copy
import pymysql
from bs4 import BeautifulSoup
from tqdm import tqdm
from pprint import pprint


# lock = threading.Lock()


# # 记录时间 创建工作目录
# startTime = time.time()
# taskID = int(startTime)
# taskPath = os.path.join(os.getcwd(), str(taskID))
# # os.mkdir(taskPath)

# os.mkdir(htmlPath)
# logPath = os.path.join(taskPath, "log.txt")


# 初始化错误列表
# indexDownFailList = []
# indexReadFailList = []


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


# 数据库类
class DB:
    host = ""
    user = ""
    __passwd = ""
    database = ""
    connection = ""
    cursor = ""

    def __init__(self, host=None, user=None, passwd="", database=None):
        self.host = host
        self.user = user
        self.__passwd = passwd
        self.database = database

    def connect(self):
        self.connection = pymysql.connect(
            self.host, self.user, self.__passwd, self.database
        )
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def rollback(self):
        self.connection.rollback()

    def execute(self, sql, args=None):
        try:
            self.cursor.execute(sql, args)
            return 1
        except pymysql.err.InterfaceError:
            self.connection.ping(reconnect=True)
            self.cursor.execute(sql, args)
            return 1
        except pymysql.Error as e:
            # print(e.args[0])
            self.rollback()
            return e

    def createTable(
        self,
        tableName,
        columns={"Name": "Type"},
        primaryKey="key",
        engine="innodb",
        de_charset="utf8mb4",
    ):
        sql = """create table `""" + tableName + """`("""
        for clName, clType in columns.items():
            sql = sql + "`" + clName + "`" + " " + clType + ","
        sql = sql + "primary key" + "(`" + primaryKey + "`)" + ")"
        sql = sql + "engine=" + engine + " " + "default charset=" + de_charset
        flag = self.execute(sql)
        self.commit()
        return flag

    def dropTable(self, tablesName):
        sql = """drop table """
        for item in tablesName:
            sql = sql + "`" + item + "`" + ","
        sql = sql[0: len(sql) - 1]
        flag = self.execute(sql)
        self.commit()
        return flag

    def insert(self, tableName, fileds, values):
        fileds = str(tuple(fileds)).replace("""'""", "`")
        values = str(tuple(values))
        tableName = "`" + tableName + "`"
        sql = """insert into """ + tableName + " "
        sql = sql + fileds + " values " + values
        flag = self.execute(sql)
        self.commit()
        return flag

    def replace(self, tableName, fileds, values):
        """替换插入"""
        fileds = str(tuple(fileds)).replace("""'""", "`")
        values = str(tuple(values))
        tableName = "`" + tableName + "`"
        sql = """REPLACE INTO """ + tableName + " "
        sql = sql + fileds + " values " + values
        flag = self.execute(sql)
        self.commit()
        return flag

    def fetchall(self):
        results = self.cursor.fetchall()
        return results

    def update(self, tableName, filed, value, whereClause):
        sql = "update " + "`" + tableName + "`" + " "
        sql = sql + "set " + "`" + filed + "`" + "=%s "
        sql = sql + whereClause
        flag = self.execute(sql, value)
        self.commit()
        return flag


# 下载一组索引页
def down1Index(pageList: list, htmlPath, indexDownFailList, proLock, startTime, taskID, taskPath, sleepTime=1, proID=0):
    # 下载
    pageCnt = 0     # 完成的任务数
    logCnt = 0
    for page in pageList:
        if page < 1:
            page = 1
        url = "https://www.everyonepiano.cn/Music.html"
        urlParams = {"p": page, "canshu": "cn_edittime", "paixu": "asc"}
        # 打印提示信息
        if proLock.acquire():
            print("Deal with page ", page)
            print()
            proLock.release()
        # 尝试下载
        res = download(url=url, params=urlParams, reFlag=2, timeout=(5, 10))
        pageCnt += 1
        if (not isinstance(res, requests.models.Response) or res.status_code != 200) and proLock.acquire():
            print(f"Page {page} fail...")
            # 更新错误列表
            indexDownFailList.append(page)
            proLock.release()
        else:
            # 保存html
            tmpPath = os.path.join(htmlPath, str(str(page) + ".html"))
            pageFile = open(tmpPath, "w", encoding="utf-8")
            pageFile.write(res.text)
            pageFile.close()
            del tmpPath
        # 写日志 延时
        if pageCnt == len(pageList)//2 or pageCnt == len(pageList):
            indexDownLog(pageList[0],
                         pageList[pageCnt-1], logCnt, indexDownFailList, proID, startTime, taskID, taskPath)
            logCnt += 1
            if pageCnt == len(pageList)//2:
                if proLock.acquire():
                    print("Process ", proID, " Sleeping... ")
                    print()
                    proLock.release()
                time.sleep(randint(30, 60))
        # 延时
        time.sleep(sleepTime)


# 多进程下载索引页
def multiDownIndex(pageList: list, proNum: int, indexDownFailList, proLock, startTime, taskID, taskPath):
    # 创建html文件保存目录
    htmlPath = os.path.join(taskPath, "html")
    try:
        os.mkdir(htmlPath)
    except Exception as e:
        print(e)
    # 根据线程数划分任务列表
    taskList = []
    if proNum > len(pageList):
        proNum = len(pageList)
    for i in range(proNum):
        taskList.append(pageList[i::proNum])

    # 开启多进程
    proList = []
    proID = 0
    kwargs = {}
    kwargs["htmlPath"] = htmlPath
    kwargs["indexDownFailList"] = indexDownFailList
    kwargs["proLock"] = proLock
    kwargs["startTime"] = startTime
    kwargs["taskID"] = taskID
    kwargs["taskPath"] = taskPath
    kwargs["sleepTime"] = proNum
    for task in taskList:
        kwargs["pageList"] = task
        kwargs["proID"] = proID
        taskProcess = multiprocessing.Process(target=down1Index, kwargs=kwargs)
        proList.append(taskProcess)
        taskProcess.start()
        proID += 1

    # 等待进程结束
    for process in proList:
        process.join()

    # 写日志
    indexDownLog(pageList[0],
                         pageList[-1], 1, indexDownFailList, proID, startTime, taskID, taskPath)


# 解析一页 获取索引数据
def analyze1Index(htmlFileList: str, indexReadFailList):

    # 创建数据库连接
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "eop")
    tableName = "main"
    try:
        db.connect()
    except Exception as e:
        for htmlFilePath in htmlFileList:
            indexReadFailList.append(htmlFilePath)
        return

    # 单进程依次处理List中的html文件
    for htmlFilePath in htmlFileList:
        # 尝试打开html文档
        try:
            htmlFile = open(htmlFilePath, "r", encoding="utf-8")
        except Exception as e:
            indexReadFailList.append(htmlFilePath)
            db.close()
            return

        # 打开成功，创建soup
        htmlSoup = BeautifulSoup(htmlFile, features="lxml")
        htmlFile.close()

        # 创建对象列表、字典
        itemList = []
        itemDic = {"id": None, "title": None, "author": None,
                   "score": None, "time": None, "description": None,
                   "eopn_page": None, "midi_page": None,
                   "pdf_page": None, "eopm_page": None,
                   "main_page": None}

        # 开始解析 排除置顶推荐
        musicBox = htmlSoup.select(".MusicIndexBox")[1:]
        for item in musicBox:
            itemDic["id"] = int(item.select(".MIMusicNO")[0].text)
            itemDic["title"] = item.select(
                ".MITitle")[0].select("a")[0]["title"].replace(" ", "-")
            itemDic["author"] = item.select(
                ".MITitle")[0].select("a")[1]["title"]
            itemDic["score"] = int(item.select(".MIMusicInfo2Num")[0].text)
            itemDic["time"] = item.select(".MIMusicUpdate")[0].text
            itemDic["description"] = item.select(
                ".MIMusicBar")[0].get_text(strip=True).replace("曲谱格式：", " ")
            itemDic["eopn_page"] = r"https://www.everyonepiano.cn/" + \
                f"""Eopn-down-{itemDic["id"]}-{itemDic["title"]}.html"""
            itemDic["midi_page"] = r"https://www.everyonepiano.cn/" + \
                f"""Midi-{itemDic["id"]}-{itemDic["title"]}.html"""
            itemDic["pdf_page"] = r"https://www.everyonepiano.cn/" + \
                f"""PDF-{itemDic["id"]}-{itemDic["title"]}.html"""
            itemDic["eopm_page"] = r"https://www.everyonepiano.cn/" + \
                f"""Eopm-down-{itemDic["id"]}-{itemDic["title"]}.html"""
            itemDic["main_page"] = r"https://www.everyonepiano.cn/" + \
                f"""Music-{itemDic["id"]}-{itemDic["title"]}.html"""
            itemList.append(copy.copy(itemDic))
            itemDic.clear()

        # 解析结束 写数据库
        for item in itemList:
            flag = db.replace(tableName, tuple(
                item.keys()), tuple(item.values()))
            if flag != 1:
                """更新失败"""
                indexReadFailList.append(htmlFilePath)

    # 关闭数据库连接
    db.close()


# 多进程解析索引数据
def multiAnalyzeIndex(htmlFileFolder: str, proNum: int, indexReadFailList, startTime, taskID, taskPath):
    # 获取html文件列表
    htmlFileList = []
    for folderName, subfolders, fileNames in os.walk(htmlFileFolder):
        for fileName in fileNames:
            if fileName.endswith(".html"):
                htmlFileList.append(os.path.join(folderName, fileName))

    # 根据线程数划分任务列表
    taskList = []
    if proNum > len(htmlFileList):
        proNum = len(htmlFileList)
    for i in range(proNum):
        taskList.append(htmlFileList[i::proNum])

    # 开启多进程
    proList = []
    for task in taskList:
        taskProcess = multiprocessing.Process(target=analyze1Index, kwargs={
                                              "htmlFileList": copy.copy(task), "indexReadFailList": indexReadFailList})
        proList.append(taskProcess)
        taskProcess.start()

    # 等待进程结束
    for process in proList:
        process.join()

    # 写日志
    indexAnalyLog(indexReadFailList, startTime, taskID, taskPath)


# 获取参数
def getParams(taskChoice: int):
    if taskChoice == 0:
        # index下载部分参数选择
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
        proNum = int(input("Process Number:\n"))
        if proNum < 1:
            proNum = 1
        if proNum > 8:
            proNum = 8

        return pageList, proNum
    elif taskChoice == 1:
        # index解析参数选择
        htmlFileFolder = input("htmlFileFolder:\n")
        if not os.path.isdir(htmlFileFolder):
            print("Wrong Dir!")
            exit()
        proNum = int(input("Process Number:\n"))
        if proNum < 1:
            proNum = 1
        if proNum > 8:
            proNum = 8

        return htmlFileFolder, proNum


# 写index下载log
def indexDownLog(startPG, endPG, CNT, indexDownFailList, proID, startTime, taskID, taskPath):
    logPath = os.path.join(
        taskPath, f"indexDownLog_{str(proID)}_{str(CNT)}.txt")

    endTime = time.time()
    spendTime = int(endTime - startTime)
    logFile = open(logPath, "w")
    logFile.write("Task ID:\n")
    logFile.write(str(taskID) + "\n")
    logFile.write("Page Range:\n")
    logFile.write(str(startPG) + "-" + str(endPG) + "\n")
    logFile.write("Failed Count:\n")
    logFile.write(str(len(indexDownFailList)) + "\n")
    logFile.write("Failed List:\n")
    logFile.write(str(indexDownFailList).replace(",", "\n") + "\n")
    logFile.write("Start Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(startTime)) + "\n")
    logFile.write("End Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(endTime)) + "\n")
    logFile.write("Time Cost:\n")
    logFile.write(str(spendTime // 3600) + "h")
    logFile.write(str((spendTime % 3600) // 60) + "m")
    logFile.write(str(spendTime % 60) + "s" + "\n")
    logFile.write("\n\n\n\n\nOriginal Failed List:\n")
    logFile.write(str(indexDownFailList))
    logFile.close()


# 写index分析log
def indexAnalyLog(indexReadFailList, startTime, taskID, taskPath):
    logPath = os.path.join(taskPath, "indexAnalyLog.txt")

    endTime = time.time()
    spendTime = int(endTime - startTime)
    logFile = open(logPath, "w")
    logFile.write("Task ID:\n")
    logFile.write(str(taskID) + "\n")
    logFile.write("Failed Count:\n")
    logFile.write(str(len(indexReadFailList)) + "\n")
    logFile.write("Failed List:\n")
    logFile.write(str(indexReadFailList).replace(",", "\n") + "\n")
    logFile.write("Start Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(startTime)) + "\n")
    logFile.write("End Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(endTime)) + "\n")
    logFile.write("Time Cost:\n")
    logFile.write(str(spendTime // 3600) + "h")
    logFile.write(str((spendTime % 3600) // 60) + "m")
    logFile.write(str(spendTime % 60) + "s" + "\n")
    logFile.write("\n\n\n\n\nOriginal Failed List:\n")
    logFile.write(str(indexReadFailList))
    logFile.close()


# 获取索引页
def test1():
    # 记录时间 创建工作目录
    startTime = time.time()
    taskID = int(startTime)
    taskPath = os.path.join(os.getcwd(), str(taskID))
    htmlPath = os.path.join(taskPath, "html")
    try:
        os.mkdir(taskPath)
        os.mkdir(htmlPath)
    except Exception as e:
        print(e)
    # 参数设置
    pageList = []
    proNum = 1
    # 开启多进程
    proLock = multiprocessing.Lock()
    with multiprocessing.Manager() as proManager:
        indexDownFailList = proManager.list([])
        multiDownIndex(pageList, proNum, indexDownFailList,
                       proLock, startTime, taskID, taskPath)
    print("Done!")


# 解析索引页
def test2():
    # 记录时间 创建工作目录
    startTime = time.time()
    taskID = int(startTime)
    taskPath = os.path.join(os.getcwd(), str(taskID))
    try:
        os.mkdir(taskPath)
    except Exception as e:
        print(e)
    # 参数设置
    htmlFileFolder = ""
    proNum = 8
    # 开启多进程
    print("正在处理...")
    with multiprocessing.Manager() as proManager:
        indexReadFailList = proManager.list([])
        multiAnalyzeIndex(htmlFileFolder, proNum,
                          indexReadFailList, startTime, taskID, taskPath)
    print("Done!")


# 主程序
def mainTask():
    # 记录时间 创建工作目录
    startTime = time.time()
    taskID = int(startTime)
    taskPath = os.path.join(os.getcwd(), str(taskID))
    try:
        os.mkdir(taskPath)
    except Exception as e:
        print(e)
    # 获取任务编号
    taskChoice = int(
        input("Which Task? 0 for indexDownload, 1 for indexAnalyze :\n"))
    if taskChoice != 1 and taskChoice != 0:
        print("Bye!")
        exit()
    # 根具任务编号执行相应的程序
    if taskChoice == 0:
        # 索引页下载任务
        # 获取参数
        pageList, proNum = getParams(taskChoice)
        # 开启多进程
        proLock = multiprocessing.Lock()
        with multiprocessing.Manager() as proManager:
            indexDownFailList = proManager.list([])
            multiDownIndex(pageList, proNum, indexDownFailList,
                           proLock, startTime, taskID, taskPath)
        print("Done!")
    elif taskChoice == 1:
        # 现有索引页分析任务
        # 获取参数
        htmlFileFolder, proNum = getParams(taskChoice)
        # 开启多进程
        print("正在处理...")
        with multiprocessing.Manager() as proManager:
            indexReadFailList = proManager.list([])
            multiAnalyzeIndex(htmlFileFolder, proNum,
                              indexReadFailList, startTime, taskID, taskPath)
        print("Done!")


if __name__ == "__main__":
    mainTask()
