# 写数据库 json to mysql
import json
import pymysql
import os
import copy
import time
import sys
from pprint import pformat

typeDic = {
    'id': 'int',
    'tags': 'text',
    'created_at': 'int',
    'creator_id': 'int',
    'author': 'text',
    'change': 'int',
    'source': 'text',
    'score': 'int',
    'md5': 'text',
    'file_size': 'int',
    'file_url': 'text',
    'is_shown_in_index': 'char(10)',
    'preview_url': 'text',
    'preview_width': 'int',
    'preview_height': 'int',
    'actual_preview_width': 'int',
    'actual_preview_height': 'int',
    'sample_url': 'text',
    'sample_width': 'int',
    'sample_height': 'int',
    'sample_file_size': 'int',
    'jpeg_url': 'text',
    'jpeg_width': 'int',
    'jpeg_height': 'int',
    'jpeg_file_size': 'int',
    'rating': 'text',
    'has_children': 'char(10)',
    'parent_id': 'int',
    'status': 'text',
    'width': 'int',
    'height': 'int',
    'is_held': 'char(10)',
    'frames_pending_string': 'text',
    'frames_pending': 'text',
    'frames_string': 'text',
    'frames': 'text'
}


class DB:
    host = ''
    user = ''
    __passwd = ''
    database = ''
    connection = ''
    cursor = ''

    def __init__(self, host=None, user=None, passwd="", database=None):
        self.host = host
        self.user = user
        self.__passwd = passwd
        self.database = database

    def connect(self):
        self.connection = pymysql.connect(self.host, self.user, self.__passwd,
                                          self.database)
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

    def createTable(self,
                    tableName,
                    columns={'Name': 'Type'},
                    primaryKey='key',
                    engine='innodb',
                    de_charset='utf8mb4'):
        sql = """create table `""" + tableName + """`("""
        for clName, clType in columns.items():
            sql = sql + '`' + clName + '`' + ' ' + clType + ','
        sql = sql + 'primary key' + '(`' + primaryKey + '`)' + ')'
        sql = sql + 'engine=' + engine + ' ' + 'default charset=' + de_charset
        flag = self.execute(sql)
        self.commit()
        return flag

    def dropTable(self, tablesName):
        sql = """drop table """
        for item in tablesName:
            sql = sql + '`' + item + '`' + ','
        sql = sql[0:len(sql) - 1]
        flag = self.execute(sql)
        self.commit()
        return flag

    def insert(self, tableName, fileds, values):
        fileds = str(tuple(fileds)).replace("""'""", '`')
        values = str(tuple(values))
        tableName = '`' + tableName + '`'
        sql = """insert into """ + tableName + ' '
        sql = sql + fileds + ' values ' + values
        flag = self.execute(sql)
        self.commit()
        return flag


def creatTable(modeJson, db, tableName):
    # json 模板
    try:
        jsFile = open(modeJson, 'r')
    except Exception:
        return -1

    data = json.load(jsFile)
    data = data[0]
    jsFile.close()

    dic1 = {}
    dic2 = {}

    # 数据类型转换 字典python --> mysql
    dic2['int'] = 'int'
    dic2['str'] = 'text'
    dic2['list'] = 'text'
    dic2['bool'] = 'char(10)'

    # 构造columns
    for k, v in data.items():
        dic1[k] = dic2[str(type(v)).replace("""<class '""",
                                            '').replace("""'>""", '')]

    # 建表
    flag = db.createTable(tableName, columns=dic1, primaryKey='id')
    return flag


def insertData(db, tableName, data):
    global typeDic
    dupList = []
    failedList = []
    for work in data:
        for k, v in work.items():
            if typeDic[k] in ['text', 'char(10)']:
                work[k] = str(v)
            if typeDic[k] == 'int' and v is None:
                work[k] = -1
        flag = db.insert(tableName, tuple(work.keys()), tuple(work.values()))
        if flag != 1:
            if flag.args[0] == 1062:
                dupList.append(work['id'])
            else:
                failedList.append(work['id'])
    return failedList, dupList


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python insertData.py [mainFolder] [tableName]')
        exit()
    mainFolder = sys.argv[1]
    tableName = sys.argv[2]
    # 链接到数据库
    db = DB('localhost', 'root', 'qhm2012@@@', 'konachan')
    db.connect()
    # 建表
    flag = db.createTable(tableName, columns=typeDic, primaryKey='id')
    if flag == 1:
        print('建表成功!')
    elif flag.args[0] == 1050:
        print('表格已存在!')
    else:
        print('建表失败!')
        print(flag.args[0], flag.args[1])
        exit()
    # 写数据
    print('正在写入数据库...')
    jsList = []
    failDic = {}
    dupDic = {}
    cnt = 0
    for folderName, subfolders, fileNames in os.walk(mainFolder):
        for fileName in fileNames:
            if fileName.endswith('.json'):
                jsList.append(os.path.join(folderName, fileName))
    for file in jsList:
        cnt += 1
        print(cnt, 'of', len(jsList))
        jsFile = open(file, 'r', encoding='utf-8')
        data = json.load(jsFile)
        jsFile.close()
        failedList, dupList = insertData(db, tableName, data)
        if len(failedList) > 0:
            failDic[file] = copy.copy(failedList)
        if len(dupList) > 0:
            dupDic[file] = copy.copy(dupList)
    db.close()
    # 写日志
    sumPath = os.path.join(os.getcwd(), str(int(time.time())) + '.log')
    sumFile = open(sumPath, 'w', encoding='utf-8')
    sumFile.write('JSON count:\n')
    sumFile.write(str(cnt) + '\n')
    sumFile.write('Failed count:\n')
    sumFile.write(str(len(failDic)) + '\n')
    sumFile.write('Faild List:\n')
    sumFile.write(pformat(failDic) + '\n')
    sumFile.write('Duplicated count:\n')
    sumFile.write(str(len(dupDic)) + '\n')
    sumFile.write('Duplicated List:\n')
    sumFile.write(pformat(dupDic))

    print('All finish!')
