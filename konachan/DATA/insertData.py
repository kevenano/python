# 写数据库 json to mysql
import json
import os
import copy
import time
import sys
from pprint import pformat
from tqdm import tqdm
from CLASS_DB import DB


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
    "is_shown_in_index": "text",
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
    "has_children": "text",
    "parent_id": "int",
    "status": "text",
    "width": "int",
    "height": "int",
    "is_held": "text",
    "frames_pending_string": "text",
    "frames_pending": "text",
    "frames_string": "text",
    "frames": "text",
    "flag_detail": "text",
}


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
            if typeDic[k] == "int" and type(v) is not int:
                work[k] = -1
        flag = db.replace(tableName, tuple(work.keys()), tuple(work.values()))
        if flag != 1:
            """更新失败"""
            failedList.append(work["id"])
    return failedList, dupList


# 更新数据库
# data必须为字典列表(直接由json.load转换得来)
# 返回操作失败的项目id
def updateData(db, tableName, data):
    global typeDic
    failedList = []
    for work in data:
        for k, v in work.items():
            if typeDic[k] in ["text", "char(10)"]:
                work[k] = str(v)
            if typeDic[k] == "int" and type(v) is not int:
                work[k] = -1
            if k == "id":
                continue
            flag = db.update(tableName, k, work[k], r"where `id`=" + str(work["id"]))
            if flag != 1:
                failedList.append(work["id"])
                break
    return failedList


# 主函数
def main():
    global typeDic
    if len(sys.argv) < 3:
        print("Usage: python insertData.py [mainFolder] [tableName]")
        exit()
    mainFolder = sys.argv[1]
    tableName = sys.argv[2]
    # 链接到数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()
    # 建表
    flag = db.createTable(tableName, columns=typeDic, primaryKey="id")
    if flag == 1:
        print("建表成功!")
    elif flag.args[0] == 1050:
        print("表格已存在!")
    else:
        print("建表失败!")
        print(flag.args[0], flag.args[1])
        exit()
    # 写数据
    print("正在写入数据库...")
    jsList = []
    failDic = {}
    dupDic = {}
    cnt = 0
    for folderName, subfolders, fileNames in os.walk(mainFolder):
        for fileName in fileNames:
            if fileName.endswith(".json"):
                jsList.append(os.path.join(folderName, fileName))
    pbar = tqdm(jsList, ncols=100)
    for file in pbar:
        cnt += 1
        # pbar.set_description(f"{cnt} of {len(jsList)}")
        jsFile = open(file, "r", encoding="utf-8")
        data = json.load(jsFile)
        jsFile.close()
        failedList, dupList = insertData(db, tableName, data)
        if len(failedList) > 0:
            failDic[file] = copy.copy(failedList)
        if len(dupList) > 0:
            dupDic[file] = copy.copy(dupList)
    db.close()
    # 写日志
    sumPath = os.path.join(os.getcwd(), str(int(time.time())) + ".log")
    sumFile = open(sumPath, "w", encoding="utf-8")
    sumFile.write("JSON count:\n")
    sumFile.write(str(cnt) + "\n")
    sumFile.write("Failed count:\n")
    sumFile.write(str(len(failDic)) + "\n")
    sumFile.write("Faild List:\n")
    if len(failDic) < 50:
        sumFile.write(pformat(failDic) + "\n")
    sumFile.write("Duplicated count:\n")
    sumFile.write(str(len(dupDic)) + "\n")
    sumFile.write("Duplicated List:\n")
    if len(dupDic) < 50:
        sumFile.write(pformat(dupDic))
    sumFile.close()
    print("All finish!")


# 测试
def test():
    global typeDic
    mainFolder = r"D:\konachan\1592901134\json"
    tableName = "test"
    # 链接到数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()
    # ..
    jsList = []
    for folderName, subfolders, fileNames in os.walk(mainFolder):
        for fileName in fileNames:
            if fileName.endswith(".json"):
                jsList.append(os.path.join(folderName, fileName))

    for file in jsList:
        jsFile = open(file, "r", encoding="utf-8")
        data = json.load(jsFile)
        jsFile.close()
        failedList, dupList = insertData(db, tableName, data)
    db.close()


if __name__ == "__main__":
    main()
