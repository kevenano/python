import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import copy
import math
import res_rc
import os
from selenium import webdriver


# unsafe 标签列表
unSafeList = [
    "~censored",
    "~panty",
    "~pussy",
    "~breats",
    "~breasts",
    "~sex",
    "~masturbation",
    "~nude",
    "~ass",
    "~nipple",
    "~underwear",
    "~panties",
    "~panty",
    "~no_bra",
    "~skirt_lift"
]

# 缩略图目录
thumbnailPath = r"D:\konachan\thumbnail"

# 源文件目录
originPath = r"I:\image"


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
        sql = sql[0 : len(sql) - 1]
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


# 主窗口
class Ui_MainWindow(object):
    resultsList = []
    currentInd = 0

    def setupUi(self, MainWindow, db, dui, browser):
        self.dui = dui
        self.browser = browser
        """布置主控件及connect函数"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 560)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(
            "#MainWindow{\n"
            "background-image: url(:/picture/source/konachan_background.png);\n"
            ";}"
        )
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.logo = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(560, 150))
        self.logo.setMaximumSize(QtCore.QSize(560, 150))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap(":/picture/source/konachan_logo.png"))
        self.logo.setScaledContents(False)
        self.logo.setObjectName("logo")
        self.gridLayout_2.addWidget(self.logo, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.searchBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.searchBox.sizePolicy().hasHeightForWidth())
        self.searchBox.setSizePolicy(sizePolicy)
        self.searchBox.setMinimumSize(QtCore.QSize(0, 115))
        self.searchBox.setMaximumSize(QtCore.QSize(16777215, 115))
        self.searchBox.setTitle("")
        self.searchBox.setObjectName("searchBox")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.searchBox)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.mianSearch = QtWidgets.QGridLayout()
        self.mianSearch.setObjectName("mianSearch")
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.mianSearch.addItem(spacerItem2, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.Go = QtWidgets.QPushButton(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Go.sizePolicy().hasHeightForWidth())
        self.Go.setSizePolicy(sizePolicy)
        self.Go.setMinimumSize(QtCore.QSize(75, 30))
        self.Go.setMaximumSize(QtCore.QSize(75, 30))
        self.Go.setStyleSheet(
            'font: 12pt "Agency FB";\n' 'font: 25 9pt "Microsoft YaHei";'
        )
        self.Go.setObjectName("Go")
        self.Go.clicked.connect(lambda: self.clickGo(db))
        self.gridLayout.addWidget(self.Go, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.Tags = QtWidgets.QLineEdit(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tags.sizePolicy().hasHeightForWidth())
        self.Tags.setSizePolicy(sizePolicy)
        self.Tags.setMinimumSize(QtCore.QSize(531, 30))
        self.Tags.setMaximumSize(QtCore.QSize(531, 30))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.Tags.setFont(font)
        self.Tags.setText("")
        self.Tags.setObjectName("Tags")
        self.gridLayout.addWidget(self.Tags, 0, 0, 1, 1)
        self.ResultCnt = QtWidgets.QLCDNumber(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResultCnt.sizePolicy().hasHeightForWidth())
        self.ResultCnt.setSizePolicy(sizePolicy)
        self.ResultCnt.setMinimumSize(QtCore.QSize(100, 30))
        self.ResultCnt.setMaximumSize(QtCore.QSize(100, 30))
        self.ResultCnt.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ResultCnt.setDigitCount(10)
        self.ResultCnt.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.ResultCnt.setProperty("value", 0.0)
        self.ResultCnt.setProperty("intValue", 0)
        self.ResultCnt.setObjectName("ResultCnt")
        self.gridLayout.addWidget(self.ResultCnt, 0, 5, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(
            20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(120, 30))
        self.label.setMaximumSize(QtCore.QSize(120, 30))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)
        self.mianSearch.addLayout(self.gridLayout, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.mianSearch.addItem(spacerItem5, 0, 2, 1, 1)
        self.gridLayout_5.addLayout(self.mianSearch, 0, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        self.gridLayout_5.addItem(spacerItem6, 1, 0, 1, 1)
        self.moreSearch = QtWidgets.QGridLayout()
        self.moreSearch.setObjectName("moreSearch")
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.moreSearch.addItem(spacerItem7, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(80, 20))
        self.label_2.setMaximumSize(QtCore.QSize(80, 80))
        self.label_2.setObjectName("label_2")
        self.moreSearch.addWidget(self.label_2, 0, 1, 1, 1)
        self.IDRange1 = QtWidgets.QSpinBox(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IDRange1.sizePolicy().hasHeightForWidth())
        self.IDRange1.setSizePolicy(sizePolicy)
        self.IDRange1.setMinimumSize(QtCore.QSize(100, 20))
        self.IDRange1.setMaximumSize(QtCore.QSize(100, 20))
        self.IDRange1.setMaximum(99999999)
        self.IDRange1.setObjectName("IDRange1")
        self.moreSearch.addWidget(self.IDRange1, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(20, 20))
        self.label_5.setMaximumSize(QtCore.QSize(20, 20))
        self.label_5.setObjectName("label_5")
        self.moreSearch.addWidget(self.label_5, 0, 3, 1, 1)
        self.IDRange2 = QtWidgets.QSpinBox(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IDRange2.sizePolicy().hasHeightForWidth())
        self.IDRange2.setSizePolicy(sizePolicy)
        self.IDRange2.setMinimumSize(QtCore.QSize(100, 20))
        self.IDRange2.setMaximumSize(QtCore.QSize(100, 20))
        self.IDRange2.setMaximum(99999999)
        self.IDRange2.setObjectName("IDRange2")
        self.moreSearch.addWidget(self.IDRange2, 0, 4, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.moreSearch.addItem(spacerItem8, 0, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(55, 20))
        self.label_3.setMaximumSize(QtCore.QSize(55, 20))
        self.label_3.setObjectName("label_3")
        self.moreSearch.addWidget(self.label_3, 0, 6, 1, 1)
        self.Order = QtWidgets.QComboBox(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Order.sizePolicy().hasHeightForWidth())
        self.Order.setSizePolicy(sizePolicy)
        self.Order.setMinimumSize(QtCore.QSize(75, 20))
        self.Order.setMaximumSize(QtCore.QSize(75, 20))
        self.Order.setStyleSheet('font: 75 10pt "Microsoft YaHei UI";')
        self.Order.setEditable(False)
        self.Order.setObjectName("Order")
        self.Order.addItem("")
        self.Order.addItem("")
        self.moreSearch.addWidget(self.Order, 0, 7, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.moreSearch.addItem(spacerItem9, 0, 8, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(90, 20))
        self.label_4.setMaximumSize(QtCore.QSize(90, 20))
        self.label_4.setObjectName("label_4")
        self.moreSearch.addWidget(self.label_4, 0, 9, 1, 1)
        self.SafeMode = QtWidgets.QCheckBox(self.searchBox)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SafeMode.sizePolicy().hasHeightForWidth())
        self.SafeMode.setSizePolicy(sizePolicy)
        self.SafeMode.setMinimumSize(QtCore.QSize(20, 20))
        self.SafeMode.setMaximumSize(QtCore.QSize(20, 20))
        self.SafeMode.setText("")
        self.SafeMode.setIconSize(QtCore.QSize(20, 20))
        self.SafeMode.setObjectName("SafeMode")
        self.moreSearch.addWidget(self.SafeMode, 0, 10, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.moreSearch.addItem(spacerItem10, 0, 11, 1, 1)
        self.gridLayout_5.addLayout(self.moreSearch, 2, 0, 1, 1)
        self.gridLayout_3.addWidget(self.searchBox, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        self.table_Widget = TableWidget()  # 实例化表格
        self.table_Widget.setPageController(1)  # 表格设置页码控制
        self.table_Widget.control_signal.connect(self.page_controller)
        self.verticalLayout.addWidget(self.table_Widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Order.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """窗口风格设置"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Go.setText(_translate("MainWindow", "Go"))
        self.label.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#a58066;">Result Count:</span></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#a58066;">ID Range:</span></p></body></html>',
            )
        )
        self.label_5.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p align="center"><span style=" font-size:12pt; font-weight:600; color:#a58066;">to</span></p></body></html>',
            )
        )
        self.label_3.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#a58066;">Order:</span></p></body></html>',
            )
        )
        self.Order.setCurrentText(_translate("MainWindow", "id"))
        self.Order.setItemText(0, _translate("MainWindow", "id"))
        self.Order.setItemText(1, _translate("MainWindow", "score"))
        self.label_4.setText(
            _translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600; color:#a58066;">Safe Mode:</span></p></body></html>',
            )
        )

    def clickGo(self, db):
        """搜索数据库，获取结果"""
        global unSafeList
        # 显示器清零
        self.ResultCnt.display(int(0))
        # 获取参数搜索
        tags = self.Tags.text()  # str
        startId = self.IDRange1.value()  # int
        endId = self.IDRange2.value()  # int
        order = self.Order.currentText()  # str
        safeMode = self.SafeMode.isChecked()  # bool
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
            self.resultsList = db.fetchall()
        # 显示结果数量
        self.ResultCnt.display(resultsCnt)
        # 更新表格
        tableTotalPage = math.ceil(resultsCnt / self.table_Widget.itemPerPage)
        self.table_Widget.totalPageValue = tableTotalPage
        self.table_Widget.curPageValue = 1
        self.refreshTable()

    def page_controller(self, signal):
        """页码控制模块"""
        # total_page = self.table_Widget.showTotalPage()
        if "home" == signal[0]:
            self.table_Widget.curPageValue = 1
        elif "pre" == signal[0]:
            # if 1 == int(signal[1]):
            # QtWidgets.QMessageBox.information(self, "提示", "已经是第一页了", QtWidgets.QMessageBox.Yes)
            # return
            if self.table_Widget.curPageValue > 1:
                self.table_Widget.curPageValue = self.table_Widget.curPageValue - 1
            else:
                self.table_Widget.curPageValue = 1
        elif "next" == signal[0]:
            # if total_page == int(signal[1]):
            # QtWidgets.QMessageBox.information(self, "提示", "已经是最后一页了", QtWidgets.QMessageBox.Yes)
            # return
            if self.table_Widget.curPageValue < self.table_Widget.totalPageValue:
                self.table_Widget.curPageValue = self.table_Widget.curPageValue + 1
            else:
                self.table_Widget.curPageValue = self.table_Widget.totalPageValue
        elif "final" == signal[0]:
            self.table_Widget.curPageValue = self.table_Widget.totalPageValue
        elif "confirm" == signal[0]:
            # if total_page < int(signal[1]) or int(signal[1]) < 0:
            # QtWidgets.QMessageBox.information(self, "提示", "跳转页码超出范围", QtWidgets.QMessageBox.Yes)
            # return
            self.table_Widget.curPageValue = self.table_Widget.skipPage.value()
        elif "check" == signal[0]:
            self.currentInd = (
                (self.table_Widget.curPageValue - 1) * self.table_Widget.itemPerPage
                + self.table_Widget.table.currentRow() * self.table_Widget.columnCount
                + self.table_Widget.table.currentColumn()
            )
            # print(self.table_Widget.curPageValue, self.currentInd)
            if self.currentInd < len(self.resultsList):
                self.dui.updateValue(self.resultsList[self.currentInd])
                self.dui.updateBox()
            return
        elif "show" == signal[0]:
            self.currentInd = (
                (self.table_Widget.curPageValue - 1) * self.table_Widget.itemPerPage
                + self.table_Widget.table.currentRow() * self.table_Widget.columnCount
                + self.table_Widget.table.currentColumn()
            )
            # print(self.table_Widget.curPageValue, self.currentInd)
            if self.currentInd < len(self.resultsList):
                self.dui.updateValue(self.resultsList[self.currentInd])
                self.dui.updateBox()
                self.showImage()
        # 更新页码控制器
        self.table_Widget.setUiText()
        # 改变表格内容
        self.changeTableContent()

    def changeTableContent(self):
        """根据当前页改变表格的内容"""
        global thumbnailPath

        curRange1 = (self.table_Widget.curPageValue - 1) * self.table_Widget.itemPerPage
        curRange2 = self.table_Widget.curPageValue * self.table_Widget.itemPerPage
        if curRange2 > len(self.resultsList):
            curRange2 = len(self.resultsList)
        curList = self.resultsList[curRange1:curRange2]
        for i in range(self.table_Widget.rowCount):
            for j in range(self.table_Widget.columnCount):
                curInd = j + i * self.table_Widget.columnCount
                self.table_Widget.table.setColumnWidth(j, 200)
                self.table_Widget.table.setRowHeight(i, 200)
                if curInd + 1 <= len(curList):
                    curID = curList[curInd][0]
                    curThumbPath = os.path.join(
                        thumbnailPath, "thumb-" + str(curID) + ".jpg"
                    )
                    # curItem = QtWidgets.QTableWidgetItem(
                    #     QtGui.QIcon(curThumbPath), str(curID)
                    # )
                    # self.table_Widget.table.setItem(i, j, curItem)
                    curItem = QtWidgets.QLabel()
                    curItem.setPixmap(QtGui.QPixmap(curThumbPath))
                    self.table_Widget.table.setCellWidget(i, j, curItem)

                else:
                    # curItem = QtWidgets.QTableWidgetItem(
                    #     QtGui.QIcon(":/picture/source/konachan_logo_small.png"), "Null"
                    # )
                    # self.table_Widget.table.setItem(i, j, curItem)
                    curItem = QtWidgets.QLabel()
                    curItem.setPixmap(
                        QtGui.QPixmap(":/picture/source/konachan_logo_small.png")
                    )
                    self.table_Widget.table.setCellWidget(i, j, curItem)

    def refreshTable(self):
        """更新页数控制器及表格内容"""
        self.table_Widget.setUiText()
        self.changeTableContent()

    def showImage(self):
        imgID = self.resultsList[self.currentInd][0]
        try:
            imgType = self.resultsList[self.currentInd][10].split(".")[-1]
        except Exception:
            return
        imgYear = 0
        # 判断年份
        if imgID >= 1 and imgID <= 50000:
            imgYear = 2009
        elif imgID >= 50001 and imgID <= 91915:
            imgYear = 2010
        elif imgID >= 91916 and imgID <= 110000:
            imgYear = 2011
        elif imgID >= 110001 and imgID <= 151836:
            imgYear = 2012
        elif imgID >= 151840 and imgID <= 175606:
            imgYear = 2013
        elif imgID >= 175607 and imgID <= 193960:
            imgYear = 2014
        elif imgID >= 193961 and imgID <= 210000:
            imgYear = 2015
        elif imgID >= 210001 and imgID <= 233400:
            imgYear = 2016
        elif imgID >= 233401 and imgID <= 257743:
            imgYear = 2017
        elif imgID >= 257744 and imgID <= 276246:
            imgYear = 2018
        elif imgID >= 276247 and imgID <= 297318:
            imgYear = 2019
        elif imgID >= 297319 and imgID <= 999999:
            imgYear = 2020
        # 构造路径
        imgPath = os.path.join(originPath, str(imgYear), str(imgID)+"."+imgType)
        if os.path.isfile(imgPath) is False:
            return
        imgUrl = r"file:///"+imgPath
        try:
            self.browser.get(imgUrl)
        except Exception:
            self.browser = webdriver.Firefox()
            self.browser.get(imgUrl)
        

# 带页码控制的表格
class TableWidget(QtWidgets.QWidget):
    control_signal = QtCore.pyqtSignal(list)

    # def __init__(self, *args, **kwargs):
    #     super(TableWidget, self).__init__(*args, **kwargs)
    #     self.__init_ui()

    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        style_sheet = """
            QtWidgets.QTableWidget {
                border: none;
                background-color:rgb(240,240,240)
            }
            QtWidgets.QPushButton{
                max-width: 18ex;
                max-height: 6ex;
                font-size: 11px;
            }
            QtWidgets.QLineEdit{
                max-width: 30px
            }
        """
        self.table = QtWidgets.QTableWidget(2, 3)  # 3 行 5 列的表格
        self.rowCount = self.table.rowCount()
        self.columnCount = self.table.columnCount()
        self.itemPerPage = self.rowCount * self.columnCount
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )  # 自适应宽度
        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet(style_sheet)
        self.table.currentCellChanged.connect(self.__check_cell)
        self.table.cellDoubleClicked.connect(self.__show_ori)

    def setPageController(self, totalPage):
        self.totalPageValue = totalPage
        self.curPageValue = 1
        """自定义页码控制器"""
        control_layout = QtWidgets.QHBoxLayout()
        homePage = QtWidgets.QPushButton("首页")
        prePage = QtWidgets.QPushButton("<上一页")
        self.curPageLabel = QtWidgets.QLabel()
        nextPage = QtWidgets.QPushButton("下一页>")
        finalPage = QtWidgets.QPushButton("尾页")
        self.totalPageLable = QtWidgets.QLabel()
        self.skipLable_0 = QtWidgets.QLabel()
        self.skipPage = QtWidgets.QSpinBox()
        self.skipPage.setMinimum(1)
        self.skipPage.setMaximum(self.totalPageValue)
        self.skipLabel_1 = QtWidgets.QLabel()
        confirmSkip = QtWidgets.QPushButton("确定")

        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)

        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPageLabel)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPageLable)
        control_layout.addWidget(self.skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(self.skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)
        self.setUiText()

    def setUiText(self):
        self.skipPage.setMaximum(self.totalPageValue)
        self.skipLable_0.setText(
            '<html><head/><body><p><span style=" color:#a58066;">跳到:</span></p></body></html>'
        )
        self.skipLabel_1.setText(
            '<html><head/><body><p><span style=" color:#a58066;">页:</span></p></body></html>'
        )
        self.curPageLabel.setText(
            f'<html><head/><body><p><span style=" color:#a58066;">{self.curPageValue}</span></p></body></html>'
        )
        self.totalPageLable.setText(
            f'<html><head/><body><p><span style=" color:#a58066;">共 {self.totalPageValue} 页:</span></p></body></html>'
        )

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home"])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre"])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next"])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final"])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm"])

    def __check_cell(self):
        """查看单元格详情"""
        self.control_signal.emit(["check"])

    def __show_ori(self):
        """查看原图"""
        self.control_signal.emit(["show"])


# 详情窗
class Ui_Detail(object):
    ID_Value = 0
    Tags_Value = ""
    Created_At_Value = 0
    Created_ID_Value = 0
    Author_Value = ""
    Score_Value = 0
    MD5_Value = ""
    File_Size_Value = 0
    Rating_Value = ""
    Has_Children_Value = ""
    Parent_ID_Value = 0
    Status_Value = ""
    Width_Value = 0
    Height_Value = 0

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(730, 620)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(711, 501))
        self.groupBox.setMaximumSize(QtCore.QSize(711, 501))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(4, 15, 699, 481))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget_2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.File_Size_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.File_Size_Box.sizePolicy().hasHeightForWidth()
        )
        self.File_Size_Box.setSizePolicy(sizePolicy)
        self.File_Size_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.File_Size_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.File_Size_Box.setObjectName("File_Size_Box")
        self.gridLayout.addWidget(self.File_Size_Box, 9, 1, 1, 1)
        self.Status_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Status_Box.sizePolicy().hasHeightForWidth())
        self.Status_Box.setSizePolicy(sizePolicy)
        self.Status_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Status_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Status_Box.setObjectName("Status_Box")
        self.gridLayout.addWidget(self.Status_Box, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setMinimumSize(QtCore.QSize(121, 18))
        self.label_16.setMaximumSize(QtCore.QSize(121, 18))
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 0, 0, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_19.sizePolicy().hasHeightForWidth())
        self.label_19.setSizePolicy(sizePolicy)
        self.label_19.setMinimumSize(QtCore.QSize(121, 18))
        self.label_19.setMaximumSize(QtCore.QSize(121, 18))
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 3, 0, 1, 1)
        self.ID_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ID_Box.sizePolicy().hasHeightForWidth())
        self.ID_Box.setSizePolicy(sizePolicy)
        self.ID_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.ID_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.ID_Box.setObjectName("ID_Box")
        self.gridLayout.addWidget(self.ID_Box, 0, 1, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QtCore.QSize(121, 18))
        self.label_18.setMaximumSize(QtCore.QSize(121, 18))
        self.label_18.setObjectName("label_18")
        self.gridLayout.addWidget(self.label_18, 2, 0, 1, 1)
        self.Height_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Height_Box.sizePolicy().hasHeightForWidth())
        self.Height_Box.setSizePolicy(sizePolicy)
        self.Height_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Height_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Height_Box.setObjectName("Height_Box")
        self.gridLayout.addWidget(self.Height_Box, 11, 1, 1, 1)
        self.Score_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Score_Box.sizePolicy().hasHeightForWidth())
        self.Score_Box.setSizePolicy(sizePolicy)
        self.Score_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Score_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Score_Box.setObjectName("Score_Box")
        self.gridLayout.addWidget(self.Score_Box, 1, 1, 1, 1)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setMinimumSize(QtCore.QSize(121, 18))
        self.label_25.setMaximumSize(QtCore.QSize(121, 18))
        self.label_25.setObjectName("label_25")
        self.gridLayout.addWidget(self.label_25, 9, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setMinimumSize(QtCore.QSize(121, 18))
        self.label_17.setMaximumSize(QtCore.QSize(121, 18))
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 1, 0, 1, 1)
        self.Author_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Author_Box.sizePolicy().hasHeightForWidth())
        self.Author_Box.setSizePolicy(sizePolicy)
        self.Author_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Author_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Author_Box.setObjectName("Author_Box")
        self.gridLayout.addWidget(self.Author_Box, 6, 1, 1, 1)
        self.label_26 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setMinimumSize(QtCore.QSize(121, 18))
        self.label_26.setMaximumSize(QtCore.QSize(121, 18))
        self.label_26.setObjectName("label_26")
        self.gridLayout.addWidget(self.label_26, 10, 0, 1, 1)
        self.MD5_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.MD5_Box.sizePolicy().hasHeightForWidth())
        self.MD5_Box.setSizePolicy(sizePolicy)
        self.MD5_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.MD5_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.MD5_Box.setObjectName("MD5_Box")
        self.gridLayout.addWidget(self.MD5_Box, 12, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_24.sizePolicy().hasHeightForWidth())
        self.label_24.setSizePolicy(sizePolicy)
        self.label_24.setMinimumSize(QtCore.QSize(121, 18))
        self.label_24.setMaximumSize(QtCore.QSize(121, 18))
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 8, 0, 1, 1)
        self.Created_At_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Created_At_Box.sizePolicy().hasHeightForWidth()
        )
        self.Created_At_Box.setSizePolicy(sizePolicy)
        self.Created_At_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Created_At_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Created_At_Box.setObjectName("Created_At_Box")
        self.gridLayout.addWidget(self.Created_At_Box, 4, 1, 1, 1)
        self.Parent_ID_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Parent_ID_Box.sizePolicy().hasHeightForWidth()
        )
        self.Parent_ID_Box.setSizePolicy(sizePolicy)
        self.Parent_ID_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Parent_ID_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Parent_ID_Box.setObjectName("Parent_ID_Box")
        self.gridLayout.addWidget(self.Parent_ID_Box, 8, 1, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_27.sizePolicy().hasHeightForWidth())
        self.label_27.setSizePolicy(sizePolicy)
        self.label_27.setMinimumSize(QtCore.QSize(121, 18))
        self.label_27.setMaximumSize(QtCore.QSize(121, 18))
        self.label_27.setObjectName("label_27")
        self.gridLayout.addWidget(self.label_27, 11, 0, 1, 1)
        self.label_22 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_22.sizePolicy().hasHeightForWidth())
        self.label_22.setSizePolicy(sizePolicy)
        self.label_22.setMinimumSize(QtCore.QSize(121, 18))
        self.label_22.setMaximumSize(QtCore.QSize(121, 18))
        self.label_22.setObjectName("label_22")
        self.gridLayout.addWidget(self.label_22, 6, 0, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setMinimumSize(QtCore.QSize(121, 18))
        self.label_23.setMaximumSize(QtCore.QSize(121, 18))
        self.label_23.setObjectName("label_23")
        self.gridLayout.addWidget(self.label_23, 7, 0, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_20.sizePolicy().hasHeightForWidth())
        self.label_20.setSizePolicy(sizePolicy)
        self.label_20.setMinimumSize(QtCore.QSize(121, 18))
        self.label_20.setMaximumSize(QtCore.QSize(121, 18))
        self.label_20.setObjectName("label_20")
        self.gridLayout.addWidget(self.label_20, 4, 0, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_21.sizePolicy().hasHeightForWidth())
        self.label_21.setSizePolicy(sizePolicy)
        self.label_21.setMinimumSize(QtCore.QSize(121, 18))
        self.label_21.setMaximumSize(QtCore.QSize(121, 18))
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 5, 0, 1, 1)
        self.Has_Children_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Has_Children_Box.sizePolicy().hasHeightForWidth()
        )
        self.Has_Children_Box.setSizePolicy(sizePolicy)
        self.Has_Children_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Has_Children_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Has_Children_Box.setObjectName("Has_Children_Box")
        self.gridLayout.addWidget(self.Has_Children_Box, 7, 1, 1, 1)
        self.Width_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Width_Box.sizePolicy().hasHeightForWidth())
        self.Width_Box.setSizePolicy(sizePolicy)
        self.Width_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Width_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Width_Box.setObjectName("Width_Box")
        self.gridLayout.addWidget(self.Width_Box, 10, 1, 1, 1)
        self.Created_ID_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Created_ID_Box.sizePolicy().hasHeightForWidth()
        )
        self.Created_ID_Box.setSizePolicy(sizePolicy)
        self.Created_ID_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Created_ID_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Created_ID_Box.setObjectName("Created_ID_Box")
        self.gridLayout.addWidget(self.Created_ID_Box, 5, 1, 1, 1)
        self.label_28 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        self.label_28.setMinimumSize(QtCore.QSize(121, 18))
        self.label_28.setMaximumSize(QtCore.QSize(121, 18))
        self.label_28.setObjectName("label_28")
        self.gridLayout.addWidget(self.label_28, 12, 0, 1, 1)
        self.Rating_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Rating_Box.sizePolicy().hasHeightForWidth())
        self.Rating_Box.setSizePolicy(sizePolicy)
        self.Rating_Box.setMinimumSize(QtCore.QSize(270, 31))
        self.Rating_Box.setMaximumSize(QtCore.QSize(270, 31))
        self.Rating_Box.setObjectName("Rating_Box")
        self.gridLayout.addWidget(self.Rating_Box, 2, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.line = QtWidgets.QFrame(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(41, 471))
        self.line.setMaximumSize(QtCore.QSize(41, 471))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_4.addWidget(self.line, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(61, 31))
        self.label_15.setMaximumSize(QtCore.QSize(61, 31))
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 0, 0, 1, 1)
        self.Tags_Box = QtWidgets.QTextBrowser(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tags_Box.sizePolicy().hasHeightForWidth())
        self.Tags_Box.setSizePolicy(sizePolicy)
        self.Tags_Box.setMinimumSize(QtCore.QSize(241, 438))
        self.Tags_Box.setMaximumSize(QtCore.QSize(241, 438))
        self.Tags_Box.setObjectName("Tags_Box")
        self.gridLayout_2.addWidget(self.Tags_Box, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 1, 1, 1)
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(711, 94))
        self.groupBox_2.setMaximumSize(QtCore.QSize(711, 94))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 30, 208, 35))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setStyleSheet('font: 75 12pt "Microsoft YaHei UI";')
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_3.addWidget(self.pushButton_2, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_3.setStyleSheet('font: 75 12pt "Microsoft YaHei UI";')
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_3.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.updateBox()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "InformationBox"))
        self.label_16.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">ID:</span></p></body></html>',
            )
        )
        self.label_19.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Status:</span></p></body></html>',
            )
        )
        self.ID_Box.setHtml(
            _translate(
                "Dialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.label_18.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Rating:</span></p></body></html>',
            )
        )
        self.label_25.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">File_Size:</span></p></body></html>',
            )
        )
        self.label_17.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Score:</span></p></body></html>',
            )
        )
        self.label_26.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Width:</span></p></body></html>',
            )
        )
        self.MD5_Box.setHtml(
            _translate(
                "Dialog",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.label_24.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Parent_ID:</span></p></body></html>',
            )
        )
        self.label_27.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Height:</span></p></body></html>',
            )
        )
        self.label_22.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Author:</span></p></body></html>',
            )
        )
        self.label_23.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Has_Children:</span></p></body></html>',
            )
        )
        self.label_20.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Created_At:</span></p></body></html>',
            )
        )
        self.label_21.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Created_ID:</span></p></body></html>',
            )
        )
        self.label_28.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">MD5:</span></p></body></html>',
            )
        )
        self.label_15.setText(
            _translate(
                "Dialog",
                '<html><head/><body><p><span style=" font-size:12pt; font-weight:600;">Tags:</span></p></body></html>',
            )
        )
        self.groupBox_2.setTitle(_translate("Dialog", "ControlBox"))
        self.pushButton_2.setText(_translate("Dialog", "Previous"))
        self.pushButton_3.setText(_translate("Dialog", "Next"))

    def updateValue(self, valueList):
        self.ID_Value = valueList[0]
        self.Tags_Value = valueList[1].replace(" ", "\n")
        self.Created_At_Value = valueList[2]
        self.Created_ID_Value = valueList[3]
        self.Author_Value = valueList[4]
        self.Score_Value = valueList[7]
        self.MD5_Value = valueList[8]
        self.File_Size_Value = valueList[9]
        self.Rating_Value = valueList[25]
        self.Has_Children_Value = valueList[26]
        self.Parent_ID_Value = valueList[27]
        self.Status_Value = valueList[28]
        self.Width_Value = valueList[29]
        self.Height_Value = valueList[30]

    def updateBox(self):
        self.ID_Box.setText(str(self.ID_Value))
        self.ID_Box.setFontPointSize(12)
        self.Tags_Box.setText(str(self.Tags_Value))
        self.Tags_Box.setFontPointSize(12)
        self.Created_At_Box.setText(str(self.Created_At_Value))
        self.Created_At_Box.setFontPointSize(12)
        self.Created_ID_Box.setText(str(self.Created_ID_Value))
        self.Created_ID_Box.setFontPointSize(12)
        self.Author_Box.setText(str(self.Author_Value))
        self.Author_Box.setFontPointSize(12)
        self.Score_Box.setText(str(self.Score_Value))
        self.Score_Box.setFontPointSize(12)
        self.MD5_Box.setText(str(self.MD5_Value))
        self.MD5_Box.setFontPointSize(12)
        self.File_Size_Box.setText(str(self.File_Size_Value))
        self.File_Size_Box.setFontPointSize(12)
        self.Rating_Box.setText(str(self.Rating_Value))
        self.Rating_Box.setFontPointSize(12)
        self.Has_Children_Box.setText(str(self.Has_Children_Value))
        self.Has_Children_Box.setFontPointSize(12)
        self.Parent_ID_Box.setText(str(self.Parent_ID_Value))
        self.Parent_ID_Box.setFontPointSize(12)
        self.Status_Box.setText(str(self.Status_Value))
        self.Status_Box.setFontPointSize(12)
        self.Width_Box.setText(str(self.Width_Value))
        self.Width_Box.setFontPointSize(12)
        self.Height_Box.setText(str(self.Height_Value))
        self.Height_Box.setFontPointSize(12)


if __name__ == "__main__":
    # 先连接到数据库
    db = DB("localhost", "root", "qo4hr[Pxm7W5", "konachan")
    db.connect()
    # 再启动GUI
    browser = webdriver.Firefox()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    detailWindow = QtWidgets.QDialog()
    dui = Ui_Detail()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, db, dui, browser)
    MainWindow.show()
    dui.setupUi(detailWindow)
    detailWindow.show()
    # 断开数据库
    db.close()
    sys.exit(app.exec_())
