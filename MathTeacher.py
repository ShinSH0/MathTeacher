from functools import partial
from PIL import ImageGrab
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from PIL.ImageQt import ImageQt

import Camera
import editImage
import getImage
import keyboard
import loadImage
import popup
import result
import solved
from Core import *


# MainWindow 설정 및 콜백함수 선언을 위한 클래스
class MyWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()

		# 마우스 이벤트 등록
		self.mousePressEvent = self.onClick
		self.mouseReleaseEvent = self.onRelease
		self.mouseMoveEvent = self.onMove

		self.Toggle = 0
		self.paint = 0
		self.edit = 0
		self.frame = QtWidgets.QLabel()
		self.pixmap = 0
		self.x = -10
		self.y = -10
		self.bx = -10
		self.by = -10
		self.mode = 0
		self.RubberBand = 0
		
		# Toggle : 마우스 클릭 플래그
		# paint : 그림판 화면 (들어왔는지 여부) 플래그
		# edit : 사진 수정 화면 (들어왔는지 여부) 플래그
		# frame : 그림판 프레임 저장 (다른 클래스에 있기 때문에 가져와야 됨)
		# pixmap : 그림판 그린 그림을 저장할 곳
		# x, y : 마우스 좌표
		# bx, by : 이전의 마우스 좌표
		# mode : 
		# - 그림판 : 펜 상태 플래그 (펜, 지우개)
		# - 사진 수정 : 마우스 클릭 플래그


	# 마우스 클릭 이벤트
	def onClick(self, event):
		self.x = event.x()
		self.y = event.y()
		if self.paint:
			# 마우스 클릭 플래그 true
			self.Toggle = True

			# 클릭했을때 점 찍기 위해 update 부름
			self.bx = self.x+1
			self.by = self.y+1
			self.update()

		if self.edit:
			if self.mode:

				if self.RubberBand:
					self.RubberBand.hide()

				self.originQPoint = event.pos()
				self.RubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)
				self.RubberBand.setGeometry(QtCore.QRect(self.originQPoint, QtCore.QSize()))
				self.RubberBand.show()


			

	# 마우스 클릭 풀었을때의 이벤트
	def onRelease(self, event):
		if self.paint:
			# 마우스 클릭 플래그 false
			self.Toggle = False

			# 저장된 점 좌표 초기화
			self.bx = -10
			self.by = -10

		if self.edit:
			if self.mode:
				self.mode = 0
			else:
				self.mode = 1
		

	# 마우스 이동 이벤트
	def onMove(self, event):
		# 마우스가 클릭된 상태고 그림판 창에 들어와있을때
		if self.Toggle and self.paint:
			self.x = event.x()
			self.y = event.y()
			# mainwindow의 update 메소드를 호출함으로서 paintEvent 호출
			self.update()

		if self.edit:
			if not isinstance(self.RubberBand,int):
				self.RubberBand.setGeometry(QtCore.QRect(self.originQPoint, event.pos()).normalized())

	# 윈도우 그릴때 발생하는 이벤트
	def paintEvent(self, e):
		# 그림판 화면에 들어와있을때
		if self.paint:
			# pixmap이 선언되지 않은 상태라면
			if self.pixmap is 0:
				# pixmap 사용 이유 : 이미지 저장 수월하게 하기 위해서,
				# QPainter 쓰는 방법을 이것밖에 몰라서
				self.pixmap = QPixmap(self.frame.width(), self.frame.height())
				# pixmap 흰색으로 채움
				self.pixmap.fill(Qt.white)
			# QPainter 호출
			painter = QPainter()
			# 그리기 시작
			painter.begin(self.pixmap)
			self.draw(painter)
			# 그리기 끝
			painter.end()
			# 수정한 pixmap을 프레임에 업데이트
			self.frame.setPixmap(self.pixmap)
			self.frame.update()

		if self.edit:
			pass
		
	# 페인트 이벤트를 위한 메소드	
	def draw(self, qp):
		# 마우스가 클릭되었을때
		if self.Toggle:
			# 펜 모드일때
			if self.mode is 0:
				qp.setPen(QPen(Qt.black, 6, Qt.SolidLine))
				qp.setBrush(QBrush(Qt.black, Qt.SolidPattern))
				qp.drawEllipse(self.x - self.frame.x(), self.y - self.frame.y()-1, 1, 1)
			# 지우개 모드일때
			elif self.mode is 1:
				qp.setPen(QPen(Qt.white, 32, Qt.SolidLine))
				qp.setBrush(QBrush(Qt.white, Qt.SolidPattern))
				qp.drawEllipse(self.x - self.frame.x(), self.y - self.frame.y(), 10, 10)

			# 점과 점사이를 부드럽게 보이기 위해 선으로 이음
			if self.bx > 0 and self.by > 0:
				path = QPainterPath()

				path.moveTo(self.bx - self.frame.x(), self.by - self.frame.y())
				path.lineTo(self.x - self.frame.x(), self.y - self.frame.y())
				qp.drawPath(path)

			# 이전의 점위치를 저장
			self.bx = self.x
			self.by = self.y
			
		
	def save(self):	
		print(MT.filename)
		currentQRect = ( self.RubberBand.geometry().adjusted(-5,-80,-5,-80) ) if not isinstance(self.RubberBand,int) else QtCore.QRect(0, 0, 800, 400)
		

		self.RubberBand = 0
		cropQPixmap = self.pixmap.copy(currentQRect)
		cropQPixmap.save('output.png')


# 사실상 메인함수

class MathTeacher(object):
	
	def init(self):
		latex2img('.') 
		self.begin= '<'
		
		self.end = '>'
		self.latex = ''
		self.app = QtWidgets.QApplication(sys.argv)
		self.MainWindow = MyWindow()
		
	    # GUI들 초기화
		self.popup_ui =popup.Ui_Form()
		self.getImage_ui = getImage.Ui_MainWindow()
		self.Camera_ui = Camera.Ui_MainWindow()
		self.editImage_ui = editImage.Ui_MainWindow()
		self.result_ui = result.Ui_MainWindow()
		self.keyboard_ui = keyboard.Ui_MainWindow()
		self.loadImage_ui = loadImage.Ui_MainWindow()
		self.cutImage_ui = result.Ui_MainWindow()
		self.solved_ui = solved.Ui_MainWindow()

		
	    # MainWindow에 getImage UI등록
		self.getImage_ui.setupUi(self.MainWindow)
		self.MainWindow.show()
		
		self.m()

		sys.exit(self.app.exec_())

	# UI 간 이동할때 이용 
	# before는 이전 UI (from)
	# after는 바꿀 UI (to)
	def changeUI(self, before, after):
		before.centralwidget.setParent(None)
		after.setupUi(self.MainWindow)
		self.MainWindow.repaint()

	# 메인 UI 설정
	def m(self):
		# 버튼 설정
		self.latex = ''
		self.getImage_ui.btn_cam.clicked.connect(self.m2c)
		self.getImage_ui.btn_edit.clicked.connect(self.m2e)
		self.getImage_ui.btn_load.clicked.connect(self.m2l)
		self.getImage_ui.btn_type.clicked.connect(self.m2t)
		self.MainWindow.paint = 0
		self.MainWindow.edit = 0
		self.MainWindow.frame = 0
		self.MainWindow.mode = 0
		self.MainWindow.pixmap = 0
	#PIL IMage를 QPixmap 형으로 바꿈
	def Image2QPixmap(self,image):
		return QPixmap.fromImage(ImageQt(image.convert("RGBA")))
	
	# clipboard의 이미지 저장
	def clip(self):
		self.clipboard_img = ImageGrab.grabclipboard()
		
		
		self.filename = None
		self.l2cu()
		
	#dialog check handler
	def dcheck(self):
		self.my_dialog.close()

	#dialog close event
	def dclose(self,evnt):
		f = open("process.txt","w")
		self.complex = self.popup_ui.lineEdit.text()
		self.matrix = self.popup_ui.lineEdit_2.text()
		self.function = self.popup_ui.lineEdit_3.text()
		self.solver = self.popup_ui.comboBox.currentText()
		self.symbs = getsymbs(self.complex,self.matrix,self.function)
		self.parsed_list,self.form_list,self.eval_list,self.priority_list = init(self.begin,self.end,"setting.txt",self.symbs)
		try:
			#latex를 sympyform으로 변환
		
			f.write("LaTeX : "+self.latex+'\n')
			self.sympyform = convertall(self.latex,self.parsed_list,self.form_list,self.eval_list,self.priority_list,self.begin,self.end)
			#sympyform을 해석함
			f.write("SympyForm : "+self.sympyform+'\n')
			self.interpreted = interpret(self.sympyform)
			f.write("Interpreted : "+self.interpreted+'\n')
			#해석한 것을 이미지로 만듦
			
			self.solved_img = latex2img(self.interpreted,imgsize= (785,365))
		except:
			#오류시 Solve Failed 출력
			self.solved_img = latex2img(r'\text{Failed\: To\:  Solve}',imgsize= (785,365))
		self.changeUI(self.result_ui, self.solved_ui)
		self.s()
	# 카메라 UI 설정
	def c(self):
		self.Camera_ui.btn_back.clicked.connect(self.c2m)
		self.Camera_ui.btn_capture.clicked.connect(self.Camera_ui.capture)
		self.Camera_ui.btn_next.clicked.connect(self.c2cu)
		
	# 그림판 UI 설정
	def e(self):
		self.editImage_ui.btn_back.clicked.connect(self.e2m)
		self.editImage_ui.btn_next.clicked.connect(self.e2r)
		self.editImage_ui.btn_pen.clicked.connect(partial(self.switchTool, 0))
		self.editImage_ui.btn_erase.clicked.connect(partial(self.switchTool, 1))
		self.MainWindow.mode = 0
		self.MainWindow.paint = 1
		self.MainWindow.frame = self.editImage_ui.lbl_frame

	# 결과창 UI 설정
	def r(self):
		self.result_ui.btn_next.clicked.connect(self.r2m)
		self.result_ui.btn_next2.clicked.connect(self.r2s)
		self.result_ui.btn_next3.clicked.connect(self.r2t)
		
		self.result_ui.lbl_frame.setPixmap(self.Image2QPixmap(self.latex_img))
		self.MainWindow.edit = 0

	# 이미지 불러오기 UI 설정
	def l(self):
		self.loadImage_ui.btn_back.clicked.connect(self.l2m)
		self.loadImage_ui.btn_dir.clicked.connect(self.openFileDialog)
		self.loadImage_ui.btn_next.clicked.connect(self.l2cu)
		self.loadImage_ui.btn_next3.clicked.connect(self.clip)

	# 풀이화면 UI설정
	def s(self):
		self.solved_ui.btn_next.clicked.connect(self.s2m)
		self.solved_ui.lbl_frame.setPixmap(self.Image2QPixmap(self.solved_img))

	# 직접입력 UI 설정
	def t(self):
		self.keyboard_ui.text_equation.setText(self.latex)
		self.keyboard_ui.btn_back.clicked.connect(self.t2m)
		self.keyboard_ui.btn_next.clicked.connect(self.t2r)

	def cu(self):
		self.cutImage_ui.btn_next.clicked.connect(self.cu2m)
		self.cutImage_ui.btn_next2.clicked.connect(self.cu2r)
		self.cutImage_ui.lbl_frame.setPixmap(self.MainWindow.pixmap)
		self.cutImage_ui.btn_next3.hide()
		self.MainWindow.edit = 1
		self.MainWindow.mode = 1

	# main -> camera
	def m2c(self):
		self.changeUI(self.getImage_ui, self.Camera_ui)
		self.c()
		self.Camera_ui.th.start()
	# main -> edit
	def m2e(self):
		self.changeUI(self.getImage_ui, self.editImage_ui)
		self.e()

	# main -> load
	def m2l(self):
		self.changeUI(self.getImage_ui, self.loadImage_ui)
		self.l()

	# main -> type
	def m2t(self):
		self.changeUI(self.getImage_ui, self.keyboard_ui)
		self.t()

	# camera -> main
	def c2m(self):
		self.Camera_ui.stop_ ()
		self.changeUI(self.Camera_ui, self.getImage_ui)
		self.m()

	# camera -> cutImage
	def c2cu(self):
		self.MainWindow.pixmap = self.Camera_ui.p
		self.Camera_ui.stop_()
		self.changeUI(self.Camera_ui, self.cutImage_ui)
		self.cu()

	# edit -> main
	def e2m(self):
		self.changeUI(self.editImage_ui, self.getImage_ui)
		self.m()
	#edit -> result
	def e2r(self):
		self.MainWindow.save()
		self.latex = img2latex('output.png')
		self.latex = displaysetting(self.latex)
		self.latex_img = latex2img(self.latex,imgsize= (785,365))
		self.changeUI(self.editImage_ui, self.result_ui)
		self.r()
	# load -> main
	def l2m(self):
		self.changeUI(self.loadImage_ui, self.getImage_ui)
		self.m()

	# load -> cutImage
	def l2cu(self):
		if not hasattr(self,'filename'):
			return

		if self.filename is None:
			self.MainWindow.pixmap = self.Image2QPixmap(center_align_img(self.clipboard_img,(785,365)))
		else:
			self.MainWindow.pixmap = self.Image2QPixmap(center_align_img(Image.open(self.filename[0]),(785,365)))
		self.changeUI(self.loadImage_ui, self.cutImage_ui)
		self.cu()
	

	# type -> main
	def t2m(self):
		self.changeUI(self.keyboard_ui, self.getImage_ui)
		self.m()

	# type -> result:
	def t2r(self):
		self.latex = self.keyboard_ui.text_equation.toPlainText()
		self.latex = displaysetting(self.latex)
		self.latex_img = latex2img(self.latex,imgsize= (785,365))
		self.changeUI(self.keyboard_ui, self.result_ui)
		self.r()

	# result -> main
	def r2m(self):
		self.changeUI(self.result_ui, self.getImage_ui)
		self.m()

	# result -> type
	def r2t(self):
		self.changeUI(self.result_ui, self.keyboard_ui)
		self.t()

	# cutImage -> main
	def cu2m(self):
		self.changeUI(self.cutImage_ui, self.getImage_ui)
		self.m()

	#result -> solved
	def r2s(self):

		# Dialog 띄우기
		self.my_dialog = QDialog()
		self.my_dialog.setModal(True)
		self.my_dialog.closeEvent = self.dclose
		self.popup_ui.setupUi(self.my_dialog)
		self.popup_ui.pushButton.clicked.connect(self.dcheck)
		self.my_dialog.show()
	
		
	#cutImage -> result
	def cu2r(self):
		self.MainWindow.save()
		self.latex = img2latex('output.png')
		self.latex = displaysetting(self.latex)
		self.latex_img = latex2img(self.latex,imgsize= (785,365))
		self.changeUI(self.cutImage_ui, self.result_ui)
		self.r()
	#solved -> main
	def s2m(self):
		self.changeUI(self.solved_ui,self.getImage_ui)
		self.m()

	# 그림판 모드 변경
	def switchTool(self, mode):
		if mode is 0:
			self.MainWindow.mode = 0
		elif mode is 1:
			self.MainWindow.mode = 1

	def openFileDialog(self):
		file_dialog = QtWidgets.QFileDialog(self.MainWindow)
		file_dialog.setNameFilters(["Images (*.png *.jpg)"])
		file_dialog.selectNameFilter("Images (*.png *.jpg)")
		if file_dialog.exec_():
			self.filename = file_dialog.selectedFiles()
			self.loadImage_ui.txt_dir.setText(self.filename[0])

if __name__ == "__main__":
	import sys
	
	MT = MathTeacher()
	MT.init()
