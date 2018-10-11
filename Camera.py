# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Camera.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


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
"image: url(:/icon/back_arrow.png);")
        self.btn_back.setText("")
        self.btn_back.setObjectName("btn_back")
        self.lbl_frame = QtWidgets.QLabel(self.centralwidget)
        self.lbl_frame.setGeometry(QtCore.QRect(5, 55, 790, 420))
        self.lbl_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lbl_frame.setText("")
        self.lbl_frame.setObjectName("lbl_frame")
        self.btn_capture = QtWidgets.QPushButton(self.centralwidget)
        self.btn_capture.setGeometry(QtCore.QRect(375, 400, 50, 50))
        self.btn_capture.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"image: url(:/icon/capture.png);")
        self.btn_capture.setText("")
        self.btn_capture.setObjectName("btn_capture")
        self.lbl_cam = QtWidgets.QLabel(self.centralwidget)
        self.lbl_cam.setGeometry(QtCore.QRect(745, 1, 49, 49))
        self.lbl_cam.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"image: url(:/icon/photo-camera.png);")
        self.lbl_cam.setText("")
        self.lbl_cam.setObjectName("lbl_cam")
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


import back_arrow_rc