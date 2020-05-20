# 整合下载与写数据库
import requests
import json
import pymysql
import os
import time
from random import randint

# 标签对应数据库中数据类型
typeDic = {
    "id": "int",
    "tags": "text",
    "created_at": "int",
    "creator_id": "int",
    "author": "text",
    "change": "int",
    "source": "text",
    "score": "int",
    "md5": "text",
    "file_size": "int",
    "file_url": "text",
    "is_shown_in_index": "char(10)",
    "preview_url": "text",
    "preview_width": "int",
    "preview_height": "int",
    "actual_preview_width": "int",
    "actual_preview_height": "int",
    "sample_url": "text",
    "sample_width": "int",
    "sample_height": "int",
    "sample_file_size": "int",
    "jpeg_url": "text",
    "jpeg_width": "int",
    "jpeg_height": "int",
    "jpeg_file_size": "int",
    "rating": "text",
    "has_children": "char(10)",
    "parent_id": "int",
    "status": "text",
    "width": "int",
    "height": "int",
    "is_held": "char(10)",
    "frames_pending_string": "text",
    "frames_pending": "text",
    "frames_string": "text",
    "frames": "text",
    "is_replaced": "tinyint(1)",
    "is_dlFailed": "tinyint(1)",
}


# Html download function
# 输入参数raw=1表示直接返回res raw=0则返回res.text
# 若下载失败， 一律返回None
def download(url, num_retries=3, headers={}, cookie="", params="", raw=0, timeout=(30, 300)):
    print("Downloading: ", url)
    if "user-agent" not in headers:
        headers["user-agent"] = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0"
    if cookie != "":
        headers["cookie"] = cookie
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        html = resp.text
        if resp.status_code >= 400:
            print("Download error: ", resp.text)
            html = None
            if num_retries and 500 <= resp.status_code < 600:
                return download(url, num_retries - 1)
    except requests.exceptions.RequestException as e:
        print("Download error!!!")
        print(e[0])
        html = None
        resp = None
    except requests.exceptions.Timeout:
        print("请求超时!")
        html = None
        resp = None
    if raw == 1:
        return resp
    else:
        return html


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
        except pymysql.Error as e:
            # print(e.args[0], e.args[1])
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

    def fetchall(self):
        results = self.cursor.fetchall()
        return results

    def update(self, tableName, filed, value, whereClause):
        sql = "update " + "`" + tableName + "`" + " "
        sql = sql + "set " + "`" + filed + "`" + "=%s "
        sql = sql + whereClause
        flag = self.execute(sql, value)
        return flag


# 向数据库中插入data
# data必须为字典列表(直接由json.load转换得来)
def insertData(db, tableName, data):
    global typeDic
    dupList = []
    failedList = []
    for work in data:
        for k, v in work.items():
            if typeDic[k] in ["text", "char(10)"]:
                work[k] = str(v)
            if typeDic[k] == "int" and v is None:
                work[k] = -1
        flag = db.insert(tableName, tuple(work.keys()), tuple(work.values()))
        if flag != 1:
            if flag.args[0] == 1062:
                dupList.append(work["id"])
            else:
                failedList.append(work["id"])
    return failedList, dupList


# 更新数据
# data必须为字典列表(直接由json.load转换得来)
# 返回操作失败的项目id
def updateData(db, tableName, data):
    global typeDic
    failedList = []
    for work in data:
        for k, v in work.items():
            if typeDic[k] in ["text", "char(10)"]:
                work[k] = str(v)
            if typeDic[k] == "int" and v is None:
                work[k] = -1
            if k == "id":
                continue
            flag = db.update(tableName, k, work[k], r"where `id`=" + str(work["id"]))
            if flag != 1:
                failedList.append(work["id"])
                break
    return failedList


# 获取参数
# mainParams: 所有参数 urlParams: 下载专用参数
# 返回:
# flag == 1 从本地json下载
# flag == 0 从网站爬取json
def getParams():
    mainParams = {}
    urlParams = {}
    flag = 0
    flag = int(input("Provide json file? 0 for NO, 1 for YES :\n"))
    if flag != 0 and flag != 1:
        print("Bye!")
        exit()
    if flag == 1:
        jsonPath = input("Json file path:\n")
        tableName = input("tableName:\n")
        mainParams["jsonPath"] = jsonPath
        mainParams["tableName"] = tableName
    else:
        tags = input("Tags:\n")
        startPage = int(input("Start Page:\n"))
        maxPage = int(input("maxPage:\n"))
        tableName = input("tableName:\n")
        if startPage < 1:
            startPage = 1
        if maxPage < 1:
            maxPage = 1
        mainParams["startPage"] = startPage
        mainParams["tags"] = tags
        mainParams["maxPage"] = maxPage
        mainParams["tableName"] = tableName
        urlParams["page"] = startPage
        urlParams["tags"] = tags

    return mainParams, urlParams, flag


# 具体下载函数.
# data: 字典列表
# starCnt: 初始计数
# 返回:
# data: 更新后的字典列表（包含下载状态信息）
# endCnt: 结束时总图片计数
def downPic(data, picPath, startCnt=0):
    picCnt = startCnt
    for item in data:
        # 如果 is_replaced 不在字典中，说明传入数据为新抓取的数据
        # 需要设置该字段
        if "is_replaced" not in item:
            item["is_replaced"] = 0
            item["is_dlFailed"] = 0
        picCnt += 1
        pic_id = item["id"]
        pic_url = item["file_url"]
        pic_size = item["file_size"]
        dtime = int(pic_size / (1024 * 1024) * 60)
        if dtime < 60:
            dtime = 60
        # 尝试下载源文件
        print("Picture count: ", picCnt, "ID: ", pic_id, "Size: ", pic_size)
        rawFile = download(url=pic_url, raw=1, timeout=(30, dtime))
        if rawFile is None:
            # 替换下载jpeg文件
            pic_url = item["jpeg_url"]
            pic_size = item["jpeg_file_size"]
            dtime = int(pic_size / (1024 * 1024) * 60)
            if dtime < 60:
                dtime = 60
            print("Try to download jpeg file instead... size: ", pic_size)
            rawFile = download(url=pic_url, raw=1, timeout=(30, dtime))
            if rawFile is None:
                # 下载失败
                print("下载失败!")
                # 更新状态标识
                item["is_dlFailed"] = 1
            else:
                # jpeg文件下载成功
                print("下载成功!")
                # 更新状态标识
                item["is_dlFailed"] = 0
                item["is_replaced"] = 1
                # 保存于本地
                tmpPath = os.path.join(picPath, str(pic_id) + pic_url[-4:])
                picFile = open(tmpPath, "wb")
                for chunk in rawFile.iter_content(100000):
                    picFile.write(chunk)
                picFile.close()
                del tmpPath
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                print()
        else:
            # 源文件下载成功
            print("下载成功!")
            # 更新状态标识
            item["is_dlFailed"] = 0
            item["is_replaced"] = 0
            # 保存于本地
            tmpPath = os.path.join(picPath, str(pic_id) + pic_url[-4:])
            picFile = open(tmpPath, "wb")
            for chunk in rawFile.iter_content(100000):
                picFile.write(chunk)
            picFile.close()
            del tmpPath
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print()
        # sleep
        time.sleep(randint(3, 5))
    # 结束时work计数
    endCnt = picCnt
    return data, endCnt


# 根据json直接下载
# 输入:
# db: 数据库
# mainParams: 主参数字典
# 返回
# dlFailed
# inFailed
# upFailed
# picCnt
def reDownload(db, mainParams):
    # 初始化相关参数
    tableName = mainParams["tableName"]
    jsonPath = mainParams["jsonPath"]
    picPath = mainParams["picPath"]
    reList = []
    dlFailed = []
    inFailed = []
    upFailed = []
    # 尝试打开json文件
    try:
        jsFile = open(jsonPath, "r", encoding='UTF-8')
    except Exception as e:
        print(e)
        return -1
    data = json.load(jsFile)        # 小心load 和 loads的区别!!!!!!!!!!
    jsFile.close()
    # 下载文件并更新数据状态标识
    data, picCnt = downPic(data, picPath)
    newData = []
    upData = []
    # 检查数据库，去重 item 字典 data 列表
    for item in data:
        workId = item["id"]
        sql = "select * from `" + tableName + "` " + "where id=" + str(workId)
        flag = db.execute(sql)
        if flag != 1:
            print(flag.args[0], flag.args[1])
            exit()
        resulte = db.fetchall()
        if len(resulte) == 0:
            newData.append(item)
        else:
            upData.append(item)
    # 写入新数据
    failedList, dupList = insertData(db, tableName, newData)
    if len(failedList) > 0:
        for item in failedList:
            inFailed.append(item)
    for item in newData:
        if item["is_replaced"] == 1:
            reList.append(item["id"])
        if item["is_dlFailed"] == 1:
            dlFailed.append(item["id"])
    # 更新旧数据
    if len(upData) > 0:
        failedList = updateData(db, mainParams["tableName"], upData)
        if len(failedList) > 0:
            for item in failedList:
                upFailed.append(item)

    return reList, dlFailed, inFailed, upFailed, picCnt


# 根据tags从网站爬取json
# 输入:
# db: 数据库
# mainParams: 主参数字典
# urlParams: 下载参数字典
# 返回
# dlFailed
# inFailed
# upFailed
# picCnt
# pageCnt
def newDownload(db, mainParams, urlParams):
    # 初始化相关参数及列表
    jsonPath = mainParams["jsonPath"]
    picPath = mainParams["picPath"]
    url = "https://konachan.com/post.json"
    picCnt = 0
    pageCnt = 0
    reList = []
    dlFailed = []
    inFailed = []
    upFailed = []
    # 循环爬取
    while True:
        # 下载并保存json
        if pageCnt == mainParams["maxPage"]:
            break
        print("Deal with page: ", urlParams["page"])
        page = download(url=url, params=urlParams)
        if page is None or len(page) < 100:
            break
        # 保存json
        pageCnt += 1
        tmpPath = os.path.join(jsonPath, str(pageCnt) + ".json")
        pageFile = open(tmpPath, "w", encoding="utf-8")
        pageFile.write(page)
        pageFile.close()
        del tmpPath
        # json转python
        data = json.loads(page)     # 小心load 和 loads的区别!!!!!!!!!!
        newData = []
        upData = []
        # 检查数据库，去重 item 字典 data 列表
        for item in data:
            workId = item["id"]
            sql = (
                "select * from `"
                + mainParams["tableName"]
                + "` "
                + "where id="
                + str(workId)
            )
            flag = db.execute(sql)
            if flag != 1:
                print(flag.args[0], flag.args[1])
                exit()
            resulte = db.fetchall()
            if len(resulte) == 0:
                newData.append(item)
            else:
                upData.append(item)
        # 下载文件并插入数据库
        if len(newData) > 0:
            newData, picCnt = downPic(newData, picPath, startCnt=picCnt)
            failedList, dupList = insertData(db, mainParams["tableName"], newData)
            # 记录
            if len(failedList) > 0:
                for item in failedList:
                    inFailed.append(item)
            for item in newData:
                if item["is_replaced"] == 1:
                    reList.append(item["id"])
                if item["is_dlFailed"] == 1:
                    dlFailed.append(item["id"])
        # 更新旧数据
        if len(upData) > 0:
            failedList = updateData(db, mainParams["tableName"], upData)
            if len(failedList) > 0:
                for item in failedList:
                    upFailed.append(item)
        # 延时并更新参数
        time.sleep(randint(10, 15))
        urlParams["page"] += 1
        print()

    return reList, dlFailed, inFailed, upFailed, picCnt, pageCnt


# 写日志
def writeLog(
    startTime,
    logPath,
    taskId,
    mainParams,
    pageCnt,
    picCnt,
    reList,
    inFailed,
    upFailed,
    dlFailed,
):
    endTime = time.time()
    spendTime = int(endTime - startTime)
    logFile = open(logPath, "w")
    logFile.write("Task ID:\n")
    logFile.write(str(taskId) + "\n")
    logFile.write("Tags:\n")
    logFile.write(mainParams["tags"] + "\n")
    logFile.write("Pages:\n")
    logFile.write(
        str(mainParams["startPage"])
        + "-"
        + str(mainParams["startPage"] + pageCnt - 1)
        + "\n"
    )
    logFile.write("New Work Count:\n")
    logFile.write(str(picCnt) + "\n")
    logFile.write("Replaced Count:\n")
    logFile.write(str(len(reList)) + "\n")
    logFile.write("Replaced List:\n")
    logFile.write(str(reList).replace(",", "\n") + "\n")
    logFile.write("Insert Failed Count:\n")
    logFile.write(str(len(inFailed)) + "\n")
    logFile.write("Insert Failed List:\n")
    logFile.write(str(inFailed).replace(",", "\n") + "\n")
    logFile.write("Update Failed Count:\n")
    logFile.write(str(len(upFailed)) + "\n")
    logFile.write("Update Failed List:\n")
    logFile.write(str(upFailed).replace(",", "\n") + "\n")
    logFile.write("Download Failed Count:\n")
    logFile.write(str(len(dlFailed)) + "\n")
    logFile.write("Download Failed List:\n")
    logFile.write(str(dlFailed).replace(",", "\n") + "\n")
    logFile.write("Start Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(startTime)) + "\n")
    logFile.write("End Time:\n")
    logFile.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(endTime)) + "\n")
    logFile.write("Time Cost:\n")
    logFile.write(str(spendTime // 3600) + "h")
    logFile.write(str((spendTime % 3600) // 60) + "m")
    logFile.write(str(spendTime % 60) + "s" + "\n")
    logFile.close()


# 主函数
def main():
    # 记录时间 创建工作目录
    startTime = time.time()
    taskId = int(startTime)
    taskPath = os.path.join(os.getcwd(), str(taskId))
    os.mkdir(taskPath)
    jsonPath = os.path.join(taskPath, "json")
    os.mkdir(jsonPath)
    picPath = os.path.join(taskPath, "picture")
    os.mkdir(picPath)
    logPath = os.path.join(taskPath, "log.txt")

    # 获取参数
    mainParams, urlParams, pflag = getParams()

    # 初始化相关参数及列表
    picCnt = 0
    pageCnt = 0
    reList = []
    dlFailed = []
    inFailed = []
    upFailed = []

    # 链接数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()

    # 建表
    flag = db.createTable(mainParams["tableName"], columns=typeDic, primaryKey="id")
    if flag == 1:
        print("建表成功!")
    elif flag.args[0] == 1050:
        print("表格已存在!")
        print()
    else:
        print("建表失败!")
        print()
        print(flag.args[0], flag.args[1])
        exit()

    # 直接从json文件下载
    if pflag == 1:
        mainParams["picPath"] = picPath
        reList, dlFailed, inFailed, upFailed, picCnt = reDownload(db, mainParams)
        pageCnt = 1

    # 从网站爬取
    if pflag == 0:
        mainParams["picPath"] = picPath
        mainParams["jsonPath"] = jsonPath
        mainParams["picPath"] = picPath
        reList, dlFailed, inFailed, upFailed, picCnt, pageCnt = newDownload(
            db, mainParams, urlParams
        )

    # 断开数据库链接
    db.close()

    # 写日志
    writeLog(
        startTime,
        logPath,
        taskId,
        mainParams,
        pageCnt,
        picCnt,
        reList,
        inFailed,
        upFailed,
        dlFailed,
    )

    # 结束
    print("\nAll finish!")


if __name__ == "__main__":
    main()
