# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'getImage.ui'
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
        self.btn_cam = QtWidgets.QPushButton(self.centralwidget)
        self.btn_cam.setGeometry(QtCore.QRect(5, 55, 390, 200))
        self.btn_cam.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/icon/photo-camera.png);")
        self.btn_cam.setText("")
        self.btn_cam.setObjectName("btn_cam")
        self.btn_edit = QtWidgets.QPushButton(self.centralwidget)
        self.btn_edit.setGeometry(QtCore.QRect(405, 55, 390, 200))
        self.btn_edit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/icon/edit.png);")
        self.btn_edit.setText("")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_load = QtWidgets.QPushButton(self.centralwidget)
        self.btn_load.setGeometry(QtCore.QRect(5, 260, 390, 200))
        self.btn_load.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/icon/folder.png);")
        self.btn_load.setText("")
        self.btn_load.setObjectName("btn_load")
        self.btn_type = QtWidgets.QPushButton(self.centralwidget)
        self.btn_type.setGeometry(QtCore.QRect(405, 260, 390, 200))
        self.btn_type.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"image: url(:/icon/keyboard.png);")
        self.btn_type.setText("")
        self.btn_type.setObjectName("btn_type")
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
