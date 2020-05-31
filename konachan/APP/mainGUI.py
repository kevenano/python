# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

import res_rc
from PyQt5 import QtCore, QtGui, QtWidgets


# 主窗口
class Ui_MainWindow(object):
    def setupUi(self, MainWindow, db):
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
        self.Go.clicked.connect(lambda:)
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
        # 显示器清零
        self.ResultCnt.display(int(0))
        # unsafe 标签列表
        unSafeList = ["~censored", "~panty", "~pussy", "~breats", "~sex", "~masturbation", "~nude"]
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
            resultsList = db.fetchall()
        # 显示结果数量
        self.ResultCnt.display(resultsCnt)

    def page_controller(self, signal):
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

        # 更新页码控制器
        self.table_Widget.setUiText()
        self.changeTableContent()  # 改变表格内容

    def changeTableContent(self):
        """根据当前页改变表格的内容"""
        pass


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
        self.table = QtWidgets.QTableWidget(3, 5)  # 3 行 5 列的表格
        self.table.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Stretch
        )  # 自适应宽度
        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet(style_sheet)

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

    # def showTotalPage(self):
    #    """返回当前总页数"""
    #    return int(self.totalPage.text()[1:-1])
