# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loadImage.ui'
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




        self.btn_back = QtWidgets.QPushButton(self.centralwidget)
        self.btn_back.setGeometry(QtCore.QRect(1, 1, 49, 49))
        self.btn_back.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-image: url(:/icon/back_arrow.png);")
        self.btn_back.setText("")
        self.btn_back.setObjectName("btn_back")




        self.lbl_edit = QtWidgets.QLabel(self.centralwidget)
        self.lbl_edit.setGeometry(QtCore.QRect(745, 1, 49, 49))
        self.lbl_edit.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"image: url(:/icon/folder.png);")
        self.lbl_edit.setText("")
        self.lbl_edit.setObjectName("lbl_edit")
        self.lbl_frame = QtWidgets.QLabel(self.centralwidget)
        self.lbl_frame.setGeometry(QtCore.QRect(5, 55, 790, 420))
        self.lbl_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lbl_frame.setText("")
        self.lbl_frame.setObjectName("lbl_frame")
        self.lbl_dir = QtWidgets.QLabel(self.centralwidget)
        self.lbl_dir.setGeometry(QtCore.QRect(20, 70, 151, 31))
        self.lbl_dir.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 17pt \"Arial\";")
        self.lbl_dir.setObjectName("lbl_dir")
        self.txt_dir = QtWidgets.QLineEdit(self.centralwidget)
        self.txt_dir.setGeometry(QtCore.QRect(20, 110, 711, 40))
        self.txt_dir.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 10pt \"Arial\";")
        self.txt_dir.setObjectName("txt_dir")
        self.btn_dir = QtWidgets.QToolButton(self.centralwidget)
        self.btn_dir.setGeometry(QtCore.QRect(740, 110, 40, 40))
        self.btn_dir.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.btn_dir.setObjectName("btn_dir")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 180, 451, 261))
        self.label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.label.setText("")
        self.label.setObjectName("label")



        self.btn_next = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next.setGeometry(QtCore.QRect(750, 390, 49, 49))
        self.btn_next.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-image: url(:/icon/next.png);")
        self.btn_next.setText("")
        self.btn_next.setObjectName("btn_next")



        self.btn_next3 = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next3.setGeometry(QtCore.QRect(20, 370, 63, 63))
        self.btn_next3.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"background-position:center center; background-repeat: no-repeat;background-image: url(resources/clipboard.png)")
        # pixmap = QPixmap("./resources/clipboard.png")
        # self.btn_next3.setIcon(QtGui.QIcon(pixmap.scaled(64, 64, QtCore.Qt.IgnoreAspectRatio)))
        
        # self.btn_next3.setIconSize(QtCore.QSize(64, 64))
        
        self.btn_next3.setText("")
        self.btn_next3.setObjectName("btn_next3")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 430, 100, 30))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "")
        self.label_2.setText("(Clipboard)")
        self.label_2.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_title.setText(_translate("MainWindow", "MathTeacher"))
        self.lbl_dir.setText(_translate("MainWindow", "Directory"))
        self.txt_dir.setText(_translate("MainWindow", "(Directory)"))
        self.btn_dir.setText(_translate("MainWindow", "..."))

import back_arrow_rc
