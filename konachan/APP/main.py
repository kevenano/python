import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import pymysql
import copy
import math
import res_rc
import os
import time
from selenium import webdriver
from mainWidget import Ui_MainWindow
from detailWidget import Ui_detailWidget


# block 标签列表
blockList = [
    "~censored",
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
    "~bra ",
    "~skirt_lift",
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
        sql = """create table """ + tableName + """`("""
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
class Ui_Main(QtCore.QObject, Ui_MainWindow):
    """主窗口"""
    resultsList = []
    currentInd = 0
    isSearching = False

    def setupUi(self, MainWindow, db, dui, browser):
        """布置控件"""
        super(Ui_Main, self).setupUi(MainWindow)
        self.Go.clicked.connect(lambda: self.clickGo(db))
        self.Tags.returnPressed.connect(lambda: self.clickGo(db))
        self.table_Widget = TableWidget()  # 实例化表格
        self.table_Widget.setPageController(1)  # 表格设置页码控制
        self.table_Widget.control_signal.connect(self.page_controller)
        self.verticalLayout_2.addWidget(self.table_Widget)

        self.dui = dui
        self.dui.control_signal.connect(self.show_controller)
        self.browser = browser

        self.retranslateUi(MainWindow)
        self.Order.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clickGo(self, db):
        """搜索数据库，获取结果"""
        global blockList
        # 显示器清零
        self.ResultCnt.display(int(0))
        # 获取参数搜索
        tags = self.Tags.text()  # str
        startId = self.IDRange1.value()  # int
        endId = self.IDRange2.value()  # int
        order = self.Order.currentText()  # str
        modeS = self.Mode_S.isChecked()     # bool
        modeQ = self.Mode_Q.isChecked()     # bool
        modeE = self.Mode_E.isChecked()     # bool
        EBL = self.EBL.isChecked()          # bool
        # print(type(tags), type(startId), type(endId), type(order), type(safeMode))
        # 构造mysql查询参数
        tags = tags.split(",")
        tags_F = []  # 包含标签
        tags_R = []  # 不包含标签
        modeList = []
        if EBL is True:
            tags_R = copy.copy(blockList)
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
        if modeS is True:
            modeList.append("s")
        if modeQ is True:
            modeList.append("q")
        if modeE is True:
            modeList.append("e")
        if len(modeList) > 0:
            sql = sql + "rating IN "+str(tuple(modeList)).replace(",)", ")")+" AND "
        sql = sql + f"id >= {startId} AND id <= {endId} "
        sql = sql + f"ORDER BY {order}"
        print(sql)
        # 创建线程
        self.thread = goThread(db, sql)
        self.thread.control_signal.connect(self.searchResult)
        self.thread.start()

    def searchResult(self, signal):
        if signal[0] == 1:
            self.resultsList = signal[2]
            resultsCnt = signal[1]
            # 显示结果数量
            self.ResultCnt.display(resultsCnt)
            # 更新表格
            tableTotalPage = math.ceil(resultsCnt / self.table_Widget.itemPerPage)
            self.table_Widget.totalPageValue = tableTotalPage
            self.table_Widget.curPageValue = 1
            self.refreshTable()
            self.Go.setDisabled(False)
        else:
            self.Go.setDisabled(True)

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
        """在浏览器中浏览原图"""
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
        imgPath = os.path.join(originPath, str(imgYear), str(imgID) + "." + imgType)
        if os.path.isfile(imgPath) is False:
            return
        imgUrl = r"file:///" + imgPath
        try:
            self.browser.get(imgUrl)
        except Exception:
            self.browser = webdriver.Firefox()
            self.browser.get(imgUrl)

    def show_controller(self, signal):
        """控制大图浏览并同步更新表格内容"""
        if "previous" == signal[0]:
            self.currentInd = self.currentInd - 1
            if self.currentInd < 0:
                self.currentInd = 1
                return
            page = math.floor(self.currentInd / self.table_Widget.itemPerPage) + 1
            row = math.floor((
                self.currentInd % self.table_Widget.itemPerPage
            ) / self.table_Widget.columnCount)
            column = (
                self.currentInd % self.table_Widget.itemPerPage
            ) % self.table_Widget.columnCount
            self.table_Widget.curPageValue = page
            self.refreshTable()
            self.table_Widget.table.setCurrentCell(row, column)
            self.showImage()
        elif "next" == signal[0]:
            self.currentInd = self.currentInd + 1
            if self.currentInd >= len(self.resultsList):
                self.currentInd = len(self.resultsList)
                return
            page = math.floor(self.currentInd / self.table_Widget.itemPerPage) + 1
            row = math.floor((
                self.currentInd % self.table_Widget.itemPerPage
            ) / self.table_Widget.columnCount)
            column = (
                self.currentInd % self.table_Widget.itemPerPage
            ) % self.table_Widget.columnCount
            self.table_Widget.curPageValue = page
            self.refreshTable()
            self.table_Widget.table.setCurrentCell(row, column)
            self.showImage()


# 多线程搜索，防假死
class goThread(QtCore.QThread):
    """多线程搜索"""
    control_signal = QtCore.pyqtSignal(list)

    def __init__(self, db, sql):
        super(goThread, self).__init__()
        self.db = db
        self.sql = sql

    def __del__(self):
        self.wait()

    def run(self):
        self.control_signal.emit([0])  # 发送信号，disable搜索按钮
        # 执行sql
        resultsList = []
        flag = self.db.execute(self.sql)
        if flag != 1:
            print(flag.args[0])
            resultsCnt = 0
        else:
            resultsCnt = self.db.cursor.rowcount
            resultsList = self.db.fetchall()
        self.control_signal.emit([1, resultsCnt, resultsList])  # 更新信号


# 详情窗
class Ui_Detail(QtCore.QObject, Ui_detailWidget):
    """详情窗"""
    control_signal = QtCore.pyqtSignal(list)

    def setupUi(self, detailWindow):
        """布置控件"""
        super(Ui_Detail, self).setupUi(detailWindow)
        self.ID_Value = 0
        self.Tags_Value = ""
        self.Created_At_Value = 0
        self.Created_ID_Value = 0
        self.Author_Value = ""
        self.Score_Value = 0
        self.MD5_Value = ""
        self.File_Size_Value = 0
        self.Rating_Value = ""
        self.Has_Children_Value = ""
        self.Parent_ID_Value = 0
        self.Status_Value = ""
        self.Width_Value = 0
        self.Height_Value = 0
        self.updateBox()
        self.previous_Button.clicked.connect(self.__previous_item)
        self.next_Button.clicked.connect(self.__next_item)

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
        # self.MD5_Box.setText(str(self.MD5_Value))
        # self.MD5_Box.setFontPointSize(12)
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

    def __previous_item(self):
        self.control_signal.emit(["previous"])

    def __next_item(self):
        self.control_signal.emit(["next"])


# 带页码控制的表格
class TableWidget(QtWidgets.QWidget):
    control_signal = QtCore.pyqtSignal(list)

    # def __init__(self, *args, **kwargs):
    #     super(TableWidget, self).__init__(*args, **kwargs)
    #     self.__init_ui()

    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        # style_sheet = """
        #     QtWidgets.QTableWidget {
        #         border: none;
        #         background-image: url(:/picture/source/konachan_background.png);
        #     }
        #     QtWidgets.QPushButton{
        #         max-width: 18ex;
        #         max-height: 6ex;
        #         font-size: 11px;
        #     }
        #     QtWidgets.QLineEdit{
        #         max-width: 30px
        #     }
        # """
        self.table = QtWidgets.QTableWidget(2, 5)  # 2 行 5 列的表格
        self.rowCount = self.table.rowCount()
        self.columnCount = self.table.columnCount()
        self.itemPerPage = self.rowCount * self.columnCount
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )  # 自适应宽度
        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet("background-image: url(:/picture/source/konachan_background.png);")
        self.table.currentCellChanged.connect(self.__check_cell)
        self.table.cellDoubleClicked.connect(self.__show_ori)

    def setPageController(self, totalPage):
        self.totalPageValue = totalPage
        self.curPageValue = 1
        """自定义页码控制器"""
        control_layout = QtWidgets.QHBoxLayout()
        self.homePageBt = QtWidgets.QPushButton("首页")
        self.prePageBt = QtWidgets.QPushButton("上一页")
        self.curPageLabel = QtWidgets.QLabel()
        self.nextPageBt = QtWidgets.QPushButton("下一页")
        self.finalPageBt = QtWidgets.QPushButton("尾页")
        self.totalPageLable = QtWidgets.QLabel()
        self.skipLable_0 = QtWidgets.QLabel()
        self.skipPage = QtWidgets.QSpinBox()
        self.skipPage.setMinimum(1)
        self.skipPage.setMaximum(self.totalPageValue)
        self.skipLabel_1 = QtWidgets.QLabel()
        self.confirmSkipBt = QtWidgets.QPushButton("确定")

        self.homePageBt.setStyleSheet(r"color: rgb(165, 128, 102);")
        self.prePageBt.setStyleSheet(r"color: rgb(165, 128, 102);")
        self.nextPageBt.setStyleSheet(r"color: rgb(165, 128, 102);")
        self.finalPageBt.setStyleSheet(r"color: rgb(165, 128, 102);")
        self.confirmSkipBt.setStyleSheet(r"color: rgb(165, 128, 102);")

        self.homePageBt.clicked.connect(self.__home_page)
        self.prePageBt.clicked.connect(self.__pre_page)
        self.nextPageBt.clicked.connect(self.__next_page)
        self.finalPageBt.clicked.connect(self.__final_page)
        self.confirmSkipBt.clicked.connect(self.__confirm_skip)

        control_layout.addStretch(1)
        control_layout.addWidget(self.homePageBt)
        control_layout.addWidget(self.prePageBt)
        control_layout.addWidget(self.curPageLabel)
        control_layout.addWidget(self.nextPageBt)
        control_layout.addWidget(self.finalPageBt)
        control_layout.addWidget(self.totalPageLable)
        control_layout.addWidget(self.skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(self.skipLabel_1)
        control_layout.addWidget(self.confirmSkipBt)
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
    dui.setupUi(detailWindow)
    ui = Ui_Main()
    ui.setupUi(MainWindow, db, dui, browser)
    MainWindow.show()
    detailWindow.show()
    # 断开数据库
    db.close()
    sys.exit(app.exec_())
