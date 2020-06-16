# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_settingDialog(object):
    def setupUi(self, settingDialog):
        settingDialog.setObjectName("settingDialog")
        settingDialog.resize(396, 205)
        settingDialog.setMinimumSize(QtCore.QSize(396, 191))
        self.verticalLayout = QtWidgets.QVBoxLayout(settingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(settingDialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.input_host = QtWidgets.QLineEdit(settingDialog)
        self.input_host.setStyleSheet('font: 12pt "新宋体";')
        self.input_host.setText("")
        self.input_host.setObjectName("input_host")
        self.gridLayout.addWidget(self.input_host, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(settingDialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.input_user = QtWidgets.QLineEdit(settingDialog)
        self.input_user.setStyleSheet('font: 12pt "新宋体";')
        self.input_user.setText("")
        self.input_user.setObjectName("input_user")
        self.gridLayout.addWidget(self.input_user, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(settingDialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.input_pass = QtWidgets.QLineEdit(settingDialog)
        self.input_pass.setStyleSheet('font: 12pt "新宋体";')
        self.input_pass.setInputMask("")
        self.input_pass.setText("")
        self.input_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_pass.setObjectName("input_pass")
        self.gridLayout.addWidget(self.input_pass, 2, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(settingDialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.input_data = QtWidgets.QLineEdit(settingDialog)
        self.input_data.setStyleSheet('font: 12pt "新宋体";')
        self.input_data.setText("")
        self.input_data.setObjectName("input_data")
        self.gridLayout.addWidget(self.input_data, 3, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(settingDialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 4, 0, 1, 1)
        self.path_origin = QtWidgets.QLineEdit(settingDialog)
        self.path_origin.setStyleSheet('font: 12pt "新宋体";')
        self.path_origin.setText("")
        self.path_origin.setObjectName("path_origin")
        self.gridLayout.addWidget(self.path_origin, 4, 1, 1, 1)
        self.choose_originPath = QtWidgets.QPushButton(settingDialog)
        self.choose_originPath.setMaximumSize(QtCore.QSize(20, 16777215))
        self.choose_originPath.setObjectName("choose_originPath")
        self.gridLayout.addWidget(self.choose_originPath, 4, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(settingDialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 1)
        self.path_thumb = QtWidgets.QLineEdit(settingDialog)
        self.path_thumb.setStyleSheet('font: 12pt "新宋体";')
        self.path_thumb.setText("")
        self.path_thumb.setObjectName("path_thumb")
        self.gridLayout.addWidget(self.path_thumb, 5, 1, 1, 1)
        self.choose_thumbPath = QtWidgets.QPushButton(settingDialog)
        self.choose_thumbPath.setMaximumSize(QtCore.QSize(20, 16777215))
        self.choose_thumbPath.setObjectName("choose_thumbPath")
        self.gridLayout.addWidget(self.choose_thumbPath, 5, 2, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(settingDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 6, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(settingDialog)
        QtCore.QMetaObject.connectSlotsByName(settingDialog)

    def retranslateUi(self, settingDialog):
        _translate = QtCore.QCoreApplication.translate
        settingDialog.setWindowTitle(_translate("settingDialog", "Dialog"))
        self.label_6.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">Host:</span></p></body></html>',
            )
        )
        self.label.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">User:</span></p></body></html>',
            )
        )
        self.label_2.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">Password:</span></p></body></html>',
            )
        )
        self.label_3.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">Database:</span></p></body></html>',
            )
        )
        self.label_4.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">Origin Path:</span></p></body></html>',
            )
        )
        self.choose_originPath.setText(_translate("settingDialog", ".."))
        self.label_5.setText(
            _translate(
                "settingDialog",
                '<html><head/><body><p align="right"><span style=" font-size:10pt; font-weight:600;">Thumbnail Path:</span></p></body></html>',
            )
        )
        self.choose_thumbPath.setText(_translate("settingDialog", ".."))