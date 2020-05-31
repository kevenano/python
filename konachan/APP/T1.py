import sys
from PyQt5 import QtWidgets
import mainGUI
from functools import partial
import pymysql
import copy


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

    def fetchall(self):
        results = self.cursor.fetchall()
        return results

    def update(self, tableName, filed, value, whereClause):
        sql = "update " + "`" + tableName + "`" + " "
        sql = sql + "set " + "`" + filed + "`" + "=%s "
        sql = sql + whereClause
        flag = self.execute(sql, value)
        return flag


def clickGo(ui, db):
    # 显示器清零
    ui.ResultCnt.display(int(0))
    # unsafe 标签列表
    unSafeList = ["~censored", "~panty", "~pussy", "~breats", "~sex", "~masturbation", "~nude"]
    # 获取参数搜索
    tags = ui.Tags.text()  # str
    startId = ui.IDRange1.value()  # int
    endId = ui.IDRange2.value()  # int
    order = ui.Order.currentText()  # str
    safeMode = ui.SafeMode.isChecked()  # bool
    # print(type(tags), type(startId), type(endId), type(order), type(safeMode))
    # 构造mysql查询参数
    tags = tags.split(",")
    tags_F = []  # 包含标签
    tags_R = []  # 不包含标签
    if safeMode is True:
        tags_R = copy.copy(unSafeList)
    for tag in tags:
        if tag != " ":
            if tag.startswith(r"~"):
                tags_R.append(tag)
            else:
                tags_F.append(tag)
    if endId < startId:
        t = endId
        endId = startId
        startId = t
        del t
    if endId == 0 and startId == 0:
        startId = 1
        endId = 99999999
    sql = "SELECT * FROM main WHERE "
    for item in tags_F:
        sql = sql + f"tags LIKE '%{item}%' AND "
    for item in tags_R:
        sql = sql + f"tags NOT LIKE '%{item[1:]}%' AND "
    sql = sql + f"id >= {startId} AND id <= {endId} "
    sql = sql + f"ORDER BY {order}"
    print(sql)
    # 执行sql
    flag = db.execute(sql)
    if flag != 1:
        print(flag.args[0])
        resultsCnt = []
    else:
        resultsCnt = db.cursor.rowcount
    # 显示结果数量
    ui.ResultCnt.display(resultsCnt)


if __name__ == "__main__":
    # 先连接到数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()
    # 再启动GUI
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = mainGUI.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    ui.Go.clicked.connect(partial(clickGo, ui, db))
    # 断开数据库
    db.close()
    sys.exit(app.exec_())
