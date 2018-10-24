from PyQt5 import QtCore, QtGui, QtWidgets
import getImage, Camera, editImage, result, keyboard, loadImage

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from functools import partial

# MainWindow 설정 및 콜백함수 선언을 위한 클래스
class MyWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super().__init__()
		self.mousePressEvent = self.onClick
		self.mouseReleaseEvent = self.onRelease
		self.mouseMoveEvent = self.onMove
		self.Toggle = 0
		self.paint = 0
		self.frame = QtWidgets.QLabel()
		self.pixmap = 0
		self.x = -10
		self.y = -10
		self.bx = -10
		self.by = -10
		self.mode = 0


	# 마우스 클릭 이벤트
	def onClick(self, event):
		# 마우스 클릭 플래그 true
		self.Toggle = True

		# 클릭했을때 점 찍기 위해 update 부름
		self.x = event.x()
		self.y = event.y()
		self.bx = self.x+1
		self.by = self.y+1
		self.update()

	# 마우스 클릭 풀었을때의 이벤트
	def onRelease(self, event):
		# 마우스 클릭 플래그 false
		self.Toggle = False

		# 저장된 점 좌표 초기화
		self.bx = -10
		self.by = -10
		

	# 마우스 이동 이벤트
	def onMove(self, event):
		# 마우스가 클릭된 상태고 그림판 창에 들어와있을때
		if self.Toggle and self.paint:
			self.x = event.x()
			self.y = event.y()
			# mainwindow의 update 메소드를 호출함으로서 paintEvent 호출
			self.update()

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
			
					


# 사실상 메인함수
class MathTeacher(object):
	def init(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.MainWindow = MyWindow()

	    # GUI들 초기화
		self.getImage_ui = getImage.Ui_MainWindow()
		self.Camera_ui = Camera.Ui_MainWindow()
		self.editImage_ui = editImage.Ui_MainWindow()
		self.result_ui = result.Ui_MainWindow()
		self.keyboard_ui = keyboard.Ui_MainWindow()
		self.loadImage_ui = loadImage.Ui_MainWindow()

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
		self.getImage_ui.btn_cam.clicked.connect(self.m2c)
		self.getImage_ui.btn_edit.clicked.connect(self.m2e)
		self.getImage_ui.btn_load.clicked.connect(self.m2l)
		self.getImage_ui.btn_type.clicked.connect(self.m2t)

		self.MainWindow.paint = 0
		self.MainWindow.frame = 0

	# 카메라 UI 설정
	def c(self):
		self.Camera_ui.btn_back.clicked.connect(self.c2m)
		self.Camera_ui.btn_capture.clicked.connect(self.Camera_ui.capture)

	# 그림판 UI 설정
	def e(self):
		self.editImage_ui.btn_back.clicked.connect(self.e2m)
		self.editImage_ui.btn_pen.clicked.connect(partial(self.switchTool, 0))
		self.editImage_ui.btn_erase.clicked.connect(partial(self.switchTool, 1))

		self.MainWindow.paint = 1
		self.MainWindow.frame = self.editImage_ui.lbl_frame

	# 이미지 불러오기 UI 설정
	def l(self):
		self.loadImage_ui.btn_back.clicked.connect(self.l2m)

	# 직접입력 UI 설정
	def t(self):
		self.keyboard_ui.btn_back.clicked.connect(self.t2m)

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

	# edit -> main
	def e2m(self):
		self.changeUI(self.editImage_ui, self.getImage_ui)
		self.m()

	# load -> main
	def l2m(self):
		self.changeUI(self.loadImage_ui, self.getImage_ui)
		self.m()
		
	# type -> main
	def t2m(self):
		self.changeUI(self.keyboard_ui, self.getImage_ui)
		self.m()

	# 그림판 모드 변경
	def switchTool(self, mode):
		if mode is 0:
			self.MainWindow.mode = 0
		elif mode is 1:
			self.MainWindow.mode = 1


if __name__ == "__main__":
	import sys
	
	MT = MathTeacher()
	MT.init()

	