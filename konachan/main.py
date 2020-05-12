# 整合下载与写数据库
import requests
import json
import pymysql
import os
import time
import shelve
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
}


# Html download function
# 输入参数raw=1表示直接返回res raw=0则返回res.text
# 若下载失败， 一律返回None
def download(url, num_retries=3, cookie="", params="", raw=0, timeout=40):
    print("Downloading: ", url)
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) "
        + "Gecko/20100101 Firefox/75.0",
        "connection": "keep-alive",
    }
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
    except requests.exceptions.RequestException:
        print("Download error!!!")
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

    def execute(self, sql):
        try:
            self.cursor.execute(sql)
            return 1
        except pymysql.Error as e:
            print(e.args[0], e.args[1])
            # print(type(e.args[0]), type(e.args[1]))
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

    def update(self, tableName, valDic={"Name": "Value"}, whereClause=""):
        sql = "update " + "`" + tableName + "`" + " set "
        cnt = 0
        for k, v in valDic.items():
            cnt += 1
            if cnt == len(valDic):
                sql = sql + "`" + k + "`" + str(v) + " "
            else:
                sql = sql + "`" + k + "`" + str(v) + ", "
        sql = sql + whereClause
        flag = self.execute(sql)
        self.commit()
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


# 获取参数
# mainParams: 所有参数 urlParams: 下载专用参数
def getParams():
    mainParams = {}
    urlParams = {}
    tags = input("Tags:\n")
    startPage = int(input("Start Page:\n"))
    maxPage = int(input("maxPage:\n"))
    tableName = input("tableName:\n")
    if startPage < 1:
        startPage = 1
    if maxPage < 1:
        maxPage = 1
    mainParams["tags"] = tags
    mainParams["page"] = startPage
    mainParams["maxPage"] = maxPage
    mainParams["tableName"] = tableName
    urlParams["tags"] = tags
    urlParams["page"] = startPage

    return mainParams, urlParams


# 具体下载函数.
# data: 字典列表
# sizeThr: 单文件大小阈值
# starCnt: 初始计数
# 返回:
# failedList: 下载失败的id列表
# endCnt: 结束时总图片计数
def downPic(data, picPath, sizeThr=10 * 1024 * 1024, startCnt=0):
    picCnt = startCnt
    failedList = []
    repList = []
    for item in data:
        picCnt += 1
        pic_id = item["id"]
        pic_url = item["file_url"]
        pic_size = item["file_size"]
        # 若源文件太大，记录下来，并更换url
        if item["file_size"] > sizeThr:
            pic_url = item["jpeg_url"]
            pic_size = item["jpeg_file_size"]
            repList.append(pic_id)
        print("Picture count: ", picCnt, "ID: ", pic_id, "Size: ", pic_size)
        rawFile = download(url=pic_url, raw=1, timeout=300)
        if rawFile is None:
            failedList.append(pic_id)
            print()
            continue
        tmpPath = os.path.join(picPath, str(pic_id) + pic_url[-4:])
        picFile = open(tmpPath, "wb")
        for chunk in rawFile.iter_content(100000):
            picFile.write(chunk)
        picFile.close()
        del tmpPath
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print()
        time.sleep(randint(3, 5))
    endCnt = picCnt
    return failedList, repList, endCnt


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
    failedDataPath = os.path.join(taskPath, "failed")
    sumPath = os.path.join(taskPath, "log.txt")

    # 获取参数
    mainParams, urlParams = getParams()

    # 初始化相关参数及列表
    url = "https://konachan.com/post.json"
    picCnt = 0
    pageCnt = 0
    reList = []
    inFailed = []
    upFailed = []
    dlFailed = []

    # 链接数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()
    # 建表
    flag = db.createTable(mainParams["tableName"], columns=typeDic, primaryKey="id")
    if flag == 1:
        print("建表成功!")
    elif flag.args[0] == 1050:
        print("表格已存在!")
    else:
        print("建表失败!")
        print(flag.args[0], flag.args[1])
        exit()

    # 循环处理所有页面
    while True:
        # 下载并保存json
        print("Deal with page: ", mainParams["page"])
        page = download(url=url, params=urlParams)
        if page is None or len(page) < 100 or pageCnt == mainParams["maxPage"]:
            break
        # 保存json
        pageCnt += 1
        tmpPath = os.path.join(jsonPath, str(pageCnt) + ".json")
        pageFile = open(tmpPath, "w", encoding="utf-8")
        pageFile.write(page)
        pageFile.close()
        del tmpPath
        # json转python
        data = json.loads(page)
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
        # 插入数据
        if len(newData) > 0:
            failedList, dupList = insertData(db, mainParams["tableName"], newData)
            if len(failedList) > 0:
                for item in failedList:
                    inFailed.append(item)
        # 更新数据
        if len(upData) > 0:
            for item in upData:
                flag = db.update(mainParams["tableName"], item)
                if flag == 1:
                    print("更新成功!")
                else:
                    print("Fail to update!")
                    print(flag[0], flag[1])
                    upFailed.append(item["id"])
        # 下载新资源
        failedList, repList, picCnt = downPic(newData, picPath, startCnt=picCnt)
        if len(failedList) > 0:
            for item in failedList:
                dlFailed.append(item["id"])
        if len(repList) > 0:
            for item in repList:
                reList.append(item["id"])
        # 延时并更新参数
        time.sleep(randint(10, 15))
        urlParams["page"] += 1
        print()

    # 保存失败id列表变量
    dataFile = shelve.open(failedDataPath)
    dataFile["reList"] = reList
    dataFile["inFailed"] = inFailed
    dataFile["upFailed"] = upFailed
    dataFile["dlFailed"] = dlFailed
    dataFile.close()

    # 写日志
    endTime = time.time()
    spendTime = int(endTime - startTime)
    sumFile = open(sumPath, 'w')
    sumFile.write('Task ID:\n')
    sumFile.write(str(taskId)+'\n')
    sumFile.write('Tags:\n')
    sumFile.write(mainParams['tags']+'\n')
    sumFile.write('Pages:\n')
    sumFile.write(str(mainParams['startPage'])+'-'+str(mainParams['startPage']+pageCnt-1)+'\n')
    sumFile.write('New Work Count:\n')
    sumFile.write(str(picCnt)+'\n')
    sumFile.write('Replaced Count:\n')
    sumFile.write(str(len(reList))+'\n')
    sumFile.write('Replaced List:\n')
    sumFile.write(str(reList).replace(',', '\n')+'\n')
    sumFile.write('Insert Failed Count:\n')
    sumFile.write(str(len(inFailed))+'\n')
    sumFile.write('Insert Failed List:\n')
    sumFile.write(str(inFailed).replace(',', '\n')+'\n')
    sumFile.write('Update Failed Count:\n')
    sumFile.write(str(len(upFailed))+'\n')
    sumFile.write('Update Failed List:\n')
    sumFile.write(str(upFailed).replace(',', '\n')+'\n')
    sumFile.write('Download Failed Count:\n')
    sumFile.write(str(len(dlFailed))+'\n')
    sumFile.write('Download Failed List:\n')
    sumFile.write(str(dlFailed).replace(',', '\n')+'\n')
    sumFile.write('Start Time:\n')
    sumFile.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(startTime))+'\n')
    sumFile.write('End Time:\n')
    sumFile.write(time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(endTime))+'\n')
    sumFile.write('Time Cost:\n')
    sumFile.write(str(spendTime//3600)+'h')
    sumFile.write(str((spendTime % 3600)//60)+'m')
    sumFile.write(str(spendTime % 60)+'s'+'\n')
    sumFile.close()
    print('All finish!')


if __name__ == '__main__':
    main()
