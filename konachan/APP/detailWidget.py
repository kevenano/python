# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detailWidget.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_detailWidget(object):
    def setupUi(self, detailWidget):
        detailWidget.setObjectName("detailWidget")
        detailWidget.resize(555, 556)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(detailWidget.sizePolicy().hasHeightForWidth())
        detailWidget.setSizePolicy(sizePolicy)
        detailWidget.setMinimumSize(QtCore.QSize(555, 556))
        detailWidget.setMaximumSize(QtCore.QSize(555, 556))
        self.verticalLayout = QtWidgets.QVBoxLayout(detailWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(detailWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(471, 481))
        self.groupBox.setMaximumSize(QtCore.QSize(9999999, 9999999))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 21, 520, 454))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_17 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_17.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_17.setObjectName("gridLayout_17")
        self.gridLayout_14 = QtWidgets.QGridLayout()
        self.gridLayout_14.setObjectName("gridLayout_14")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_16 = QtWidgets.QLabel(self.layoutWidget)
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
        self.ID_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ID_Box.sizePolicy().hasHeightForWidth())
        self.ID_Box.setSizePolicy(sizePolicy)
        self.ID_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.ID_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.ID_Box.setAutoFormatting(QtWidgets.QTextEdit.AutoNone)
        self.ID_Box.setObjectName("ID_Box")
        self.gridLayout.addWidget(self.ID_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_17 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_2.addWidget(self.label_17, 0, 0, 1, 1)
        self.Score_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Score_Box.sizePolicy().hasHeightForWidth())
        self.Score_Box.setSizePolicy(sizePolicy)
        self.Score_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Score_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Score_Box.setObjectName("Score_Box")
        self.gridLayout_2.addWidget(self.Score_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_18 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_4.addWidget(self.label_18, 0, 0, 1, 1)
        self.Rating_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Rating_Box.sizePolicy().hasHeightForWidth())
        self.Rating_Box.setSizePolicy(sizePolicy)
        self.Rating_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Rating_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Rating_Box.setObjectName("Rating_Box")
        self.gridLayout_4.addWidget(self.Rating_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.label_19 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_5.addWidget(self.label_19, 0, 0, 1, 1)
        self.Status_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Status_Box.sizePolicy().hasHeightForWidth())
        self.Status_Box.setSizePolicy(sizePolicy)
        self.Status_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Status_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Status_Box.setObjectName("Status_Box")
        self.gridLayout_5.addWidget(self.Status_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_5, 3, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.label_20 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_6.addWidget(self.label_20, 0, 0, 1, 1)
        self.Created_At_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Created_At_Box.sizePolicy().hasHeightForWidth()
        )
        self.Created_At_Box.setSizePolicy(sizePolicy)
        self.Created_At_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Created_At_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Created_At_Box.setObjectName("Created_At_Box")
        self.gridLayout_6.addWidget(self.Created_At_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_6, 4, 0, 1, 1)
        self.gridLayout_7 = QtWidgets.QGridLayout()
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.label_21 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_7.addWidget(self.label_21, 0, 0, 1, 1)
        self.Created_ID_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Created_ID_Box.sizePolicy().hasHeightForWidth()
        )
        self.Created_ID_Box.setSizePolicy(sizePolicy)
        self.Created_ID_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Created_ID_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Created_ID_Box.setObjectName("Created_ID_Box")
        self.gridLayout_7.addWidget(self.Created_ID_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_7, 5, 0, 1, 1)
        self.gridLayout_8 = QtWidgets.QGridLayout()
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.label_22 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_8.addWidget(self.label_22, 0, 0, 1, 1)
        self.Author_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Author_Box.sizePolicy().hasHeightForWidth())
        self.Author_Box.setSizePolicy(sizePolicy)
        self.Author_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Author_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Author_Box.setObjectName("Author_Box")
        self.gridLayout_8.addWidget(self.Author_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_8, 6, 0, 1, 1)
        self.gridLayout_9 = QtWidgets.QGridLayout()
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_9.addWidget(self.label_23, 0, 0, 1, 1)
        self.Has_Children_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Has_Children_Box.sizePolicy().hasHeightForWidth()
        )
        self.Has_Children_Box.setSizePolicy(sizePolicy)
        self.Has_Children_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Has_Children_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Has_Children_Box.setObjectName("Has_Children_Box")
        self.gridLayout_9.addWidget(self.Has_Children_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_9, 7, 0, 1, 1)
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_24 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_10.addWidget(self.label_24, 0, 0, 1, 1)
        self.Parent_ID_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Parent_ID_Box.sizePolicy().hasHeightForWidth()
        )
        self.Parent_ID_Box.setSizePolicy(sizePolicy)
        self.Parent_ID_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Parent_ID_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Parent_ID_Box.setObjectName("Parent_ID_Box")
        self.gridLayout_10.addWidget(self.Parent_ID_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_10, 8, 0, 1, 1)
        self.gridLayout_11 = QtWidgets.QGridLayout()
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_11.addWidget(self.label_25, 0, 0, 1, 1)
        self.File_Size_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.File_Size_Box.sizePolicy().hasHeightForWidth()
        )
        self.File_Size_Box.setSizePolicy(sizePolicy)
        self.File_Size_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.File_Size_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.File_Size_Box.setObjectName("File_Size_Box")
        self.gridLayout_11.addWidget(self.File_Size_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_11, 9, 0, 1, 1)
        self.gridLayout_12 = QtWidgets.QGridLayout()
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.label_26 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_12.addWidget(self.label_26, 0, 0, 1, 1)
        self.Width_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Width_Box.sizePolicy().hasHeightForWidth())
        self.Width_Box.setSizePolicy(sizePolicy)
        self.Width_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Width_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Width_Box.setObjectName("Width_Box")
        self.gridLayout_12.addWidget(self.Width_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_12, 10, 0, 1, 1)
        self.gridLayout_13 = QtWidgets.QGridLayout()
        self.gridLayout_13.setObjectName("gridLayout_13")
        self.label_27 = QtWidgets.QLabel(self.layoutWidget)
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
        self.gridLayout_13.addWidget(self.label_27, 0, 0, 1, 1)
        self.Height_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Height_Box.sizePolicy().hasHeightForWidth())
        self.Height_Box.setSizePolicy(sizePolicy)
        self.Height_Box.setMinimumSize(QtCore.QSize(150, 30))
        self.Height_Box.setMaximumSize(QtCore.QSize(150, 30))
        self.Height_Box.setObjectName("Height_Box")
        self.gridLayout_13.addWidget(self.Height_Box, 0, 1, 1, 1)
        self.gridLayout_14.addLayout(self.gridLayout_13, 11, 0, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_14, 0, 0, 1, 1)
        self.gridLayout_16 = QtWidgets.QGridLayout()
        self.gridLayout_16.setObjectName("gridLayout_16")
        self.line = QtWidgets.QFrame(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(40, 450))
        self.line.setMaximumSize(QtCore.QSize(40, 450))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_16.addWidget(self.line, 0, 0, 1, 1)
        self.gridLayout_15 = QtWidgets.QGridLayout()
        self.gridLayout_15.setObjectName("gridLayout_15")
        self.label_15 = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_15.sizePolicy().hasHeightForWidth())
        self.label_15.setSizePolicy(sizePolicy)
        self.label_15.setMinimumSize(QtCore.QSize(51, 31))
        self.label_15.setMaximumSize(QtCore.QSize(51, 9999))
        self.label_15.setObjectName("label_15")
        self.gridLayout_15.addWidget(self.label_15, 0, 0, 1, 1)
        self.Tags_Box = QtWidgets.QTextBrowser(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Tags_Box.sizePolicy().hasHeightForWidth())
        self.Tags_Box.setSizePolicy(sizePolicy)
        self.Tags_Box.setMinimumSize(QtCore.QSize(181, 400))
        self.Tags_Box.setMaximumSize(QtCore.QSize(181, 500))
        self.Tags_Box.setObjectName("Tags_Box")
        self.gridLayout_15.addWidget(self.Tags_Box, 1, 0, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_15, 0, 1, 1, 1)
        self.gridLayout_17.addLayout(self.gridLayout_16, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(detailWidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(9999999, 9999999))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(160, 10, 208, 35))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.previous_Button = QtWidgets.QPushButton(self.layoutWidget1)
        self.previous_Button.setStyleSheet('font: 75 12pt "Microsoft YaHei UI";')
        self.previous_Button.setObjectName("previous_Button")
        self.gridLayout_3.addWidget(self.previous_Button, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.next_Button = QtWidgets.QPushButton(self.layoutWidget1)
        self.next_Button.setStyleSheet('font: 75 12pt "Microsoft YaHei UI";')
        self.next_Button.setObjectName("next_Button")
        self.gridLayout_3.addWidget(self.next_Button, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(detailWidget)
        QtCore.QMetaObject.connectSlotsByName(detailWidget)

    def retranslateUi(self, detailWidget):
        _translate = QtCore.QCoreApplication.translate
        detailWidget.setWindowTitle(_translate("detailWidget", "Dialog"))
        self.groupBox.setTitle(_translate("detailWidget", "InformationBox"))
        self.label_16.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">ID:</span></p></body></html>',
            )
        )
        self.ID_Box.setHtml(
            _translate(
                "detailWidget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.label_17.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Score:</span></p></body></html>',
            )
        )
        self.label_18.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Rating:</span></p></body></html>',
            )
        )
        self.label_19.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Status:</span></p></body></html>',
            )
        )
        self.label_20.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Created_At:</span></p></body></html>',
            )
        )
        self.Created_At_Box.setHtml(
            _translate(
                "detailWidget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.label_21.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Created_ID:</span></p></body></html>',
            )
        )
        self.label_22.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Author:</span></p></body></html>',
            )
        )
        self.Author_Box.setHtml(
            _translate(
                "detailWidget",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
                '<p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><br /></p></body></html>',
            )
        )
        self.label_23.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Has_Children:</span></p></body></html>',
            )
        )
        self.label_24.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Parent_ID:</span></p></body></html>',
            )
        )
        self.label_25.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">File_Size:</span></p></body></html>',
            )
        )
        self.label_26.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Width:</span></p></body></html>',
            )
        )
        self.label_27.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Height:</span></p></body></html>',
            )
        )
        self.label_15.setText(
            _translate(
                "detailWidget",
                '<html><head/><body><p align="right"><span style=" font-size:12pt; font-weight:600;">Tags:</span></p></body></html>',
            )
        )
        self.groupBox_2.setTitle(_translate("detailWidget", "ControlBox"))
        self.previous_Button.setText(_translate("detailWidget", "Previous"))
        self.next_Button.setText(_translate("detailWidget", "Next"))