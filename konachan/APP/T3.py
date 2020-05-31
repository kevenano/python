from PyQt5 import QtCore, QtGui, QtWidgets


class TableWidget(QtWidgets.QWidget):
    control_signal = QtCore.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super(TableWidget, self).__init__(*args, **kwargs)
        self.__init_ui()

    def __init_ui(self):
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
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # 自适应宽度
        self.__layout = QtWidgets.QVBoxLayout()
        self.__layout.addWidget(self.table)
        self.setLayout(self.__layout)
        self.setStyleSheet(style_sheet)

    def setPageController(self, page):
        """自定义页码控制器"""
        control_layout = QtWidgets.QHBoxLayout()
        homePage = QtWidgets.QPushButton("首页")
        prePage = QtWidgets.QPushButton("<上一页")
        self.curPage = QtWidgets.QLabel("1")
        nextPage = QtWidgets.QPushButton("下一页>")
        finalPage = QtWidgets.QPushButton("尾页")
        self.totalPage = QtWidgets.QLabel("共" + str(page) + "页")
        skipLable_0 = QtWidgets.QLabel("跳到")
        self.skipPage = QtWidgets.QLineEdit()
        skipLabel_1 = QtWidgets.QLabel("页")
        confirmSkip = QtWidgets.QPushButton("确定")
        homePage.clicked.connect(self.__home_page)
        prePage.clicked.connect(self.__pre_page)
        nextPage.clicked.connect(self.__next_page)
        finalPage.clicked.connect(self.__final_page)
        confirmSkip.clicked.connect(self.__confirm_skip)
        control_layout.addStretch(1)
        control_layout.addWidget(homePage)
        control_layout.addWidget(prePage)
        control_layout.addWidget(self.curPage)
        control_layout.addWidget(nextPage)
        control_layout.addWidget(finalPage)
        control_layout.addWidget(self.totalPage)
        control_layout.addWidget(skipLable_0)
        control_layout.addWidget(self.skipPage)
        control_layout.addWidget(skipLabel_1)
        control_layout.addWidget(confirmSkip)
        control_layout.addStretch(1)
        self.__layout.addLayout(control_layout)

    def __home_page(self):
        """点击首页信号"""
        self.control_signal.emit(["home", self.curPage.text()])

    def __pre_page(self):
        """点击上一页信号"""
        self.control_signal.emit(["pre", self.curPage.text()])

    def __next_page(self):
        """点击下一页信号"""
        self.control_signal.emit(["next", self.curPage.text()])

    def __final_page(self):
        """尾页点击信号"""
        self.control_signal.emit(["final", self.curPage.text()])

    def __confirm_skip(self):
        """跳转页码确定"""
        self.control_signal.emit(["confirm", self.skipPage.text()])

    def showTotalPage(self):
        """返回当前总页数"""
        return int(self.totalPage.text()[1:-1])

