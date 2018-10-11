from PyQt5 import QtCore, QtGui, QtWidgets
import getImage, Camera, editImage, result, keyboard, loadImage

class MathTeacher(object):
	def init(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.MainWindow = QtWidgets.QMainWindow()

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

	def changeUI(self, before, after):
		#self.MainWindow = 0
		#self.MainWindow = QtWidgets.QMainWindow()
		before.centralwidget.setParent(None)
		after.setupUi(self.MainWindow)
		self.MainWindow.repaint()

	def m(self):
		# GUI간의 연결 설정
		self.getImage_ui.btn_cam.clicked.connect(self.m2c)
		self.getImage_ui.btn_edit.clicked.connect(self.m2e)
		self.getImage_ui.btn_load.clicked.connect(self.m2l)
		self.getImage_ui.btn_type.clicked.connect(self.m2t)

	def c(self):
		self.Camera_ui.btn_back.clicked.connect(self.c2m)

	def e(self):
		self.editImage_ui.btn_back.clicked.connect(self.e2m)

	def l(self):
		self.loadImage_ui.btn_back.clicked.connect(self.l2m)

	def t(self):
		self.keyboard_ui.btn_back.clicked.connect(self.t2m)

	def m2c(self):
		# main -> camera
		self.changeUI(self.getImage_ui, self.Camera_ui)
		self.c()

	def m2e(self):
		# main -> edit
		self.changeUI(self.getImage_ui, self.editImage_ui)
		self.e()

	def m2l(self):
		# main -> load
		self.changeUI(self.getImage_ui, self.loadImage_ui)
		self.l()

	def m2t(self):
		# main -> type
		self.changeUI(self.getImage_ui, self.keyboard_ui)
		self.t()

	def c2m(self):
		# camera -> main
		self.changeUI(self.Camera_ui, self.getImage_ui)
		self.m()

	def e2m(self):
		# edit -> main
		self.changeUI(self.editImage_ui, self.getImage_ui)
		self.m()
		pass

	def l2m(self):
		# load -> main
		self.changeUI(self.loadImage_ui, self.getImage_ui)
		self.m()
		pass

	def t2m(self):
		# type -> main
		self.changeUI(self.keyboard_ui, self.getImage_ui)
		self.m()
		pass

if __name__ == "__main__":
	import sys
	
	MT = MathTeacher()
	MT.init()

	