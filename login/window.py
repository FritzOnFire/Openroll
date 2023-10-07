from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import global_vars.vars as g

class LoginWindow(QMainWindow):
	can_drag: bool = True

	def __init__(self, parent=None):
		super().__init__(parent)

		# Set the size of the main window
		self.setGeometry(0, 0, 790, 525)

		# Disable resizing
		self.setFixedSize(self.size())

		self.setWindowTitle('Openroll')

		# # Move window on drag
		self.dragPos = QPoint()
		def mousePressEvent(event):
			self.dragPos = event.globalPos()
		def mouseMoveEvent(event):
			if event.buttons() == Qt.LeftButton and self.can_drag:
				self.move(self.pos() + event.globalPos() - self.dragPos)
				self.dragPos = event.globalPos()
		self.mousePressEvent = mousePressEvent
		self.mouseMoveEvent = mouseMoveEvent

		# Center the window
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		self.setContentsMargins(0, 0, 0, 0)

		self.setStyleSheet("""
			QMainWindow {
				background-color: #000000;
			}
		""")

		self.container = QWidget(self)
		self.setCentralWidget(self.container)
		self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
		self.container.setAttribute(Qt.WA_NativeWindow)

		self.top_layout = QVBoxLayout(self.container)
		self.top_layout.setSpacing(0)
		self.top_layout.setContentsMargins(0, 0, 0, 0)

		self.login_label = QLabel('Log In', self.container)
		self.login_label.setAlignment(Qt.AlignCenter)
		self.login_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				font-size: 34px;
				font-weight: 500;
				max-height: 76px;
				min-height: 76px;
			}
		""")
		self.top_layout.addWidget(self.login_label, 0, Qt.AlignHCenter | Qt.AlignTop)

		self.form_container = QWidget(self.container)
		self.form_container.setContentsMargins(0, 0, 0, 0)
		self.form_container.setObjectName('form_container')
		self.form_container.setStyleSheet("""
			QWidget#form_container {
				background-color: #141519;
				max-width: 496px;
				min-width: 496px;
				max-height: 235px;
				min-height: 235px;
			}
		""")

		self.form_layout = QBoxLayout(QBoxLayout.TopToBottom, self.form_container)
		self.form_layout.setContentsMargins(48, 40, 48, 40)

		self.createLoginForm(self.form_container, self.form_layout)
		self.top_layout.addWidget(self.form_container, 0, Qt.AlignHCenter | Qt.AlignTop)

		self.createLoginButton(self.container, self.top_layout)
		self.loadAssets()
		self.addCloseButton()

	def createLoginForm(self, container: QWidget, layout: QBoxLayout):
		self.user_name_input = QLineEdit(container)
		self.user_name_input.setPlaceholderText('Email or Username')
		self.user_name_input.setStyleSheet("""
			QLineEdit {
				color: #ffffff;
				background-color: #141519;
				max-height: 34px;
				font-size: 18px;
				border: none;
				border-bottom: 2px solid #59595b;
				padding-top: 4px;
				padding-bottom: 2px;
			}
			QLineEdit:focus {
				border-bottom: 2px solid #f47521;
			}
		""")
		layout.addWidget(self.user_name_input)

		self.password_input = QLineEdit(container)
		self.password_input.setPlaceholderText('Password')
		self.password_input.setStyleSheet("""
			QLineEdit {
				color: #ffffff;
				background-color: #141519;
				max-height: 34px;
				font-size: 18px;
				border: none;
				border-bottom: 2px solid #59595b;
				padding-top: 4px;
				padding-bottom: 2px;
			}
			QLineEdit:focus {
				border-bottom: 2px solid #f47521;
			}
		""")
		layout.addWidget(self.password_input)

	def createLoginButton(self, container: QWidget, layout: QBoxLayout):
		self.login_button = QPushButton('LOG IN', container)
		self.login_button.setStyleSheet("""
			QPushButton {
				background-color: #f47521;
				color: #000000;
				font-size: 14px;
				font-weight: 900;
				padding: 16px;
				border: none;
				max-width: 120px;
				min-width: 120px;
				margin-top: 20px;
			}
		""")
		self.login_button.clicked.connect(self.login)

		# Disable can_drag when hovering over the login button
		def enterEvent(event):
			self.can_drag = False
		def leaveEvent(event):
			self.can_drag = True
		self.login_button.enterEvent = enterEvent
		self.login_button.leaveEvent = leaveEvent

		layout.addWidget(self.login_button, 1, Qt.AlignHCenter | Qt.AlignTop)


	def login(self):
		# Check if username or password is empty
		if self.user_name_input.text() == '':
			self.user_name_input.setStyleSheet("""
				QLabel {
					color: #f47521;
					border-color: #f47521;
				}
			""")
			return

		if self.password_input.text() == '':
			self.password_input.setStyleSheet("""
				QLabel {
					color: #f47521;
					border-color: #f47521;
				}
			""")
			return

		if g.crunchyroll.login(self.user_name_input.text(), self.password_input.text()) == True:
			# Close the login window we are done
			self.close()

		print('Failed to login')

	def addCloseButton(self):
		self.close_button = QPushButton('×', self.container)
		self.close_button.setStyleSheet("""
			QPushButton {
				color: #ffffff;
				font-size: 20px;
				border: none;
				padding-bottom: 1px;
				max-width: 21px;
				min-width: 21px;
				max-height: 21px;
				min-height: 21px;
				margin-left: 765px;
				margin-top: 5px;
			}
			QPushButton:hover {
				background-color: #f47521;
			}
		""")
		self.close_button.clicked.connect(self.close)

		# Disable can_drag when hovering over the close button
		def enterEvent(event):
			self.can_drag = False
		def leaveEvent(event):
			self.can_drag = True
		self.close_button.enterEvent = enterEvent
		self.close_button.leaveEvent = leaveEvent

		self.setWindowFlag(Qt.FramelessWindowHint)

	def loadAssets(self):
		# Load hime over everything to the left of the login form
		self.hime_image = QLabel(self.container)
		self.hime_image.setPixmap(QPixmap('assets/log-in-hime@2x.png'))
		self.hime_image.setAlignment(Qt.AlignCenter)
		self.hime_image.setStyleSheet("""
			QLabel {
				max-height: 488px;
				min-height: 488px;
				max-width: 186px;
				min-width: 186px;
				margin-top: 32px;
				margin-left: 5px;
			}
		""")
		# Make image clickthrough
		self.hime_image.setAttribute(Qt.WA_TransparentForMouseEvents)

		# Load yuzu over everything to the bottom right of the login form
		self.yuzu_image = QLabel(self.container)
		self.yuzu_image.setPixmap(QPixmap('assets/log-in-yuzu@2x.png'))
		self.yuzu_image.setAlignment(Qt.AlignCenter)
		self.yuzu_image.setStyleSheet("""
			QLabel {
				max-height: 108px;
				min-height: 108px;
				max-width: 118px;
				min-width: 118px;
				margin-top: 417px;
				margin-left: 613px;
			}
		""")
		# Make image clickthrough
		self.yuzu_image.setAttribute(Qt.WA_TransparentForMouseEvents)
