# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'keyboard.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import math
import MTlist

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        self.folders = [
        'Accent', 'Array', 'Arrow', 'Brace' ,'Escaped', 'Greek', 'Integral', 
        'Log Limit', 'Operator', 'Relational', 'Root Fraction', 'Space', 'Subscript', 
        'Sum', 'Symbol','Triangle Function']

        self.lens = {
        'Accent' : 5,
        'Array' : 1,
        'Arrow' : 7,
        'Brace' : 8,
        'Escaped' : 10,
        'Greek' : 29,
        'Integral' : 12,
        'Log Limit' : 6,
        'Operator' : 17,
        'Relational' : 21,
        'Root Fraction' : 4,
        'Space' : 6,
        'Subscript' : 4,
        'Sum' : 12,
        'Symbol' : 16,
        'Triangle Function' : 6
        }

        self.panels = []
        self.buttons = []
        self.page = 0


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
"image: url(:/icon/keyboard.png);")
        self.lbl_edit.setText("")
        self.lbl_edit.setObjectName("lbl_edit")
        self.lbl_frame = QtWidgets.QLabel(self.centralwidget)
        self.lbl_frame.setGeometry(QtCore.QRect(5, 55, 790, 420))
        self.lbl_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lbl_frame.setText("")
        self.lbl_frame.setObjectName("lbl_frame")
        self.btn_next = QtWidgets.QPushButton(self.centralwidget)
        self.btn_next.setGeometry(QtCore.QRect(750, 390, 49, 49))
        self.btn_next.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n"
"border-image: url(:/icon/next.png);")
        self.btn_next.setText("")
        self.btn_next.setObjectName("btn_next")
        self.text_equation = QtWidgets.QTextEdit(self.centralwidget)
        self.text_equation.setGeometry(QtCore.QRect(10, 230, 581, 221))
        self.text_equation.setStyleSheet("background-color: rgb(250, 250, 250);")
        self.text_equation.setObjectName("text_equation")
    
        x, y = 10, 60
        width, height = 63, 75
        ascX, ascY = 68, 80

        self.buttons_op = []

        for i in range(len(self.folders)):
            button = QtWidgets.QPushButton(self.centralwidget)
            button.setGeometry(QtCore.QRect(x+(ascX*(i%8)), y+(ascY*int(i/8)), width, height))
            button.setStyleSheet("background-color: rgba(255, 255, 255, 0);background-position:center center; background-repeat: no-repeat;"+"background-image: url(image/%s/0.png)"%(self.folders[i]))
            button.setText("")
            button.setObjectName("btn_%d"%(i))

            # pixmap = QPixmap("./image/%s/0.png"%(self.folders[i]))
            # button.setIcon(QtGui.QIcon(pixmap.scaled(50, 50, QtCore.Qt.IgnoreAspectRatio)))

            # button.setIconSize(QtCore.QSize(50, 50))

            button.clicked.connect(partial(self.changePanel, self.folders[i]))

            self.buttons_op.append(button)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.text_equation.setFocus()
        self.changePanel(self.folders[0])

    # 버튼 선택 패널을 바꾸기 위함 (패널을 만듬)
    # stri : 폴더 이름
    def changePanel(self, stri):
        self.page = 0

        for p in self.panels:
            p.hide()
        for b in self.buttons:
            b.hide()

        self.buttons.clear()
        self.panels.clear()
        # 폴더 개수만큼 반복
        for i in range(len(self.folders)):

            # 인자가 폴더 리스트 i번째 와 같으면
            if stri == self.folders[i]:
                # 일치한 폴더의 image 파일 개수 받아옴
                count = self.lens[self.folders[i]]

                # 한 페이지 당 10개 이미지 
                # 페이지 개수를 구함
                page = math.ceil(count / 10)

                # 페이지 개수만큼 반복
                for i2 in range(page):

                    # 패널 만듬
                    panel = QtWidgets.QFrame(self.centralwidget)
                    panel.setGeometry(QtCore.QRect(600,70,185,300))
                    panel.setStyleSheet("background-color: rgb(255,255,255);")
                    panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
                    panel.setObjectName("panel_%s_%d"%(stri,i2))

                    # 10번 반복 (패널 내부에 버튼 넣기 위함)
                    for i3 in range(1, 11):

                        # 마지막 페이지 버튼 개수 초과 방지
                        if i2+1 == page:
                            if i3-1 == (count-1) % 10 + 1:
                                break

                        # x, y 좌표 구함
                        x, y = 5, 5
                        ascX, ascY = 90, 55

                        if i3 % 2 == 0:
                            x = x + ascX
                            y = y + ascY * (math.floor(i3 / 2)-1)

                        else:
                            y = y + ascY * math.floor(i3 / 2)

                        
                        # 버튼 만듬
                        button = QtWidgets.QPushButton(panel)
                        button.setGeometry(QtCore.QRect(x, y-5, 85, 60))
                        button.setStyleSheet("background-color: rgba(255, 255, 255, 0);background-position:center center; background-repeat: no-repeat;"+"background-position:center center; background-repeat: no-repeat;background-image: url(image/%s/%d.png)"%(stri, i2*10+i3))
                        button.setText("")
                        button.setObjectName("btn_%s_%d"%(stri,i2*10+i3))

                        # 이미지 받아옴
                        # pixmap = QPixmap("./image/%s/%d.png"%(stri, i2*10+i3))
                        # button.setIcon(QtGui.QIcon(pixmap.scaled(50, 50, QtCore.Qt.IgnoreAspectRatio)))
                        # button.setIconSize(QtCore.QSize(45, 45))

                        button.clicked.connect(partial(self.addText, stri, i2 * 10 + i3))

                        self.buttons.append(button)

                    # 페이지 넘김 버튼 만듬
                    # 페이지가 1보다 많을때
                    if page > 1:
                        # 첫 페이지 일때
                        if i2 == 0:
                            button = QtWidgets.QPushButton(panel)
                            button.setGeometry(QtCore.QRect(150, 280, 25, 15))
                            button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nbackground-position:center center; background-repeat: no-repeat;background-image: url(resources/n.png)")
                            button.setText("")
                           # button.setIcon(QtGui.QIcon("./resources/n.png"))
                           # button.setIconSize(QtCore.QSize(15, 12))

                            button.clicked.connect(partial(self.changePage, 1))

                            self.buttons.append(button)
                        # 마지막 페이지 일때
                        elif i2 == page-1:
                            button = QtWidgets.QPushButton(panel)
                            button.setGeometry(QtCore.QRect(5, 280, 25, 15))
                            button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nbackground-position:center center; background-repeat: no-repeat;background-image: url(resources/b.png)")
                            button.setText("")
                            # button.setIcon(QtGui.QIcon("./resources/b.png"))
                            # button.setIconSize(QtCore.QSize(15, 12))

                            button.clicked.connect(partial(self.changePage, -1))

                            self.buttons.append(button)
                        # 그 외
                        else:
                            button = QtWidgets.QPushButton(panel)
                            button.setGeometry(QtCore.QRect(5, 280, 25, 15))
                            button.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nbackground-position:center center; background-repeat: no-repeat;background-image: url(resources/b.png)")
                            button.setText("")
                            # button.setIcon(QtGui.QIcon("./resources/b.png"))
                            # button.setIconSize(QtCore.QSize(15, 12))

                            button2 = QtWidgets.QPushButton(panel)
                            button2.setGeometry(QtCore.QRect(150, 280, 25, 15))
                            button2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\nbackground-position:center center; background-repeat: no-repeat;background-image: url(resources/n.png)")
                            button2.setText("")
                            # button2.setIcon(QtGui.QIcon("./resources/n.png"))
                            # button2.setIconSize(QtCore.QSize(15, 12))

                            button.clicked.connect(partial(self.changePage, -1))
                            button2.clicked.connect(partial(self.changePage, 1))

                            self.buttons.append(button)
                            self.buttons.append(button2)


                    # 패널 배열에 추가
                    self.panels.append(panel)
                    panel.show()
                self.raise2(self.panels[0])

    # 버튼 선택 패널의 버튼이 눌러졌을때 
    # str_folder : 폴더이름
    # idx : 폴더 내 파일의 번호
    def addText(self, str_folder, idx):
        info = MTlist.getInfo(str_folder, idx)
        #self.text_equation.append(info[0])
        self.append_(info[1],info[2])

    # 버튼 선택 패널의 페이지 이동 버튼이 눌러졌을때
    # page : 1이 들어오면 다음 페이지 -1이 들어오면 이전 페이지
    def changePage(self, page):
        self.page = self.page + page
        self.raise2(self.panels[self.page])

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_title.setText(_translate("MainWindow", "MathTeacher"))

    def append_(self, strstr,cursorback=0):
        self.text_equation.insertPlainText( strstr)
        cursor = self.text_equation.textCursor()
        cursor.setPosition(cursor.anchor()-cursorback)
        self.text_equation.setTextCursor(cursor)
        self.raise2()

    def raise2(self, widget=None):
        if widget is not None:
            widget.raise_()
            widget.repaint()
        self.text_equation.setFocus()

import back_arrow_rc
