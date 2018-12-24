# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'result.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lbl_title = QtWidgets.QLabel(self.centralwidget)
        self.lbl_title.setGeometry(QtCore.QRect(0, 0, 800, 50))
        self.lbl_title.setStyleSheet("background-color: rgb(100, 178, 244);\n"
"font: 75 18pt \"Arial\";\n"
"color: rgb(0, 0, 0);\n"
"")
        self.lbl_title.setTextFormat(QtCore.Qt.PlainText)
        self.lbl_title.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_title.setObjectName("lbl_title")
        self.lbl_frame = QtWidgets.QLabel(self.centralwidget)
        self.lbl_frame.setGeometry(QtCore.QRect(5, 55, 790, 420))
        self.lbl_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lbl_frame.setText("")
        self.lbl_frame.setObjectName("lbl_frame")
        self.btn_next = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next.setGeometry(QtCore.QRect(745, 1, 49, 49))
        self.btn_next.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-image: url(:/icon/home.png);")
        self.btn_next.setText("")
        self.btn_next.setObjectName("btn_next")

        self.btn_next2 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next2.setGeometry(QtCore.QRect(750, 390, 49, 49))
        self.btn_next2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-image: url(:/icon/next.png);")
        self.btn_next2.setText("")
        self.btn_next2.setObjectName("btn_next2")


        self.btn_next3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next3.setGeometry(QtCore.QRect(10, 384, 63, 63))
        self.btn_next3.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nborder-image: url(resources/keyboard.png)")
        # pixmap = QPixmap("./resources/keyboard.png")
        # self.btn_next3.setIcon(QtGui.QIcon(pixmap.scaled(64, 64, QtCore.Qt.IgnoreAspectRatio)))
        
        # self.btn_next3.setIconSize(QtCore.QSize(64, 64))
        
        self.btn_next3.setText("")
        self.btn_next3.setObjectName("btn_next3")


        MainWindow.setCentralWidget(self.centralwidget)


        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_title.setText(_translate("MainWindow", "MathTeacher"))

import back_arrow_rc
