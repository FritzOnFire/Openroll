from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import global_vars.vars as g
from utils.layout import addCloseButton, addMoveOnDrag

class LoginWindow(QMainWindow):
	can_drag: bool = True
	close_button: QPushButton = None

	def __init__(self, parent=None):
		super().__init__(parent)

		# Set the size of the main window
		self.setGeometry(0, 0, g.scale(790), g.scale(525))

		# Disable resizing
		self.setFixedSize(self.size())

		self.setWindowTitle('Openroll')
		self.setWindowFlag(Qt.FramelessWindowHint)

		addMoveOnDrag(self)

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
		self.login_label.setFixedHeight(g.scale(76))
		font = self.login_label.font()
		font.setPixelSize(g.scale(34))
		font.setWeight(QFont.Weight.Medium)
		self.login_label.setFont(font)
		self.login_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		self.top_layout.addWidget(self.login_label, 0, Qt.AlignHCenter | Qt.AlignTop)

		self.form_container = QWidget(self.container)
		self.form_container.setContentsMargins(0, 0, 0, 0)
		self.form_container.setObjectName('form_container')
		self.form_container.setFixedSize(g.scale(496), g.scale(235))
		self.form_container.setStyleSheet("""
			QWidget#form_container {
				background-color: #141519;
			}
		""")

		self.form_layout = QBoxLayout(QBoxLayout.TopToBottom, self.form_container)
		self.form_layout.setContentsMargins(g.scale(48), g.scale(40), g.scale(48), g.scale(40))

		self.createLoginForm(self.form_container, self.form_layout)
		self.top_layout.addWidget(self.form_container, 0, Qt.AlignHCenter | Qt.AlignTop)

		self.createLoginButton(self.container, self.top_layout)
		self.loadAssets()
		addCloseButton(self)

	def createLoginForm(self, container: QWidget, layout: QBoxLayout):
		self.user_name_input = QLineEdit(container)
		self.user_name_input.setPlaceholderText('Email or Username')
		self.user_name_input.font().setPointSize(g.scale(18))
		self.setInputStyle(self.user_name_input)

		layout.addWidget(self.user_name_input)

		self.password_input = QLineEdit(container)
		self.password_input.setPlaceholderText('Password')
		self.password_input.font().setPointSize(g.scale(18))
		self.password_input.setEchoMode(QLineEdit.Password)
		self.setInputStyle(self.password_input)

		layout.addWidget(self.password_input)

	def createLoginButton(self, container: QWidget, layout: QBoxLayout):
		self.login_button = QPushButton('LOG IN', container)
		self.login_button.setFixedWidth(g.scale(120))
		font = self.login_button.font()
		font.setPixelSize(g.scale(14))
		font.setWeight(QFont.Weight.Black)
		self.login_button.setFont(font)

		self.login_button.setStyleSheet("""
			QPushButton {
				background-color: #f47521;
				color: #000000;
				border: none;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
		"""
		f"""
				padding: {g.scale(16)}px;
				margin-top: {g.scale(20)}px;
		"""
		"""
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
		fail = False

		# Check if username or password is empty
		if self.user_name_input.text() == '':
			self.setInputStyle(self.user_name_input, '#f47521', '#f47521')
			fail = True

		if self.password_input.text() == '':
			self.setInputStyle(self.password_input, '#f47521', '#f47521')
			fail = True

		if fail:
			return

		try:
			g.crunchyroll.login(self.user_name_input.text(), self.password_input.text())
		except Exception as e:
			print(e)
			return

		if g.crunchyroll.logged_in == True:
			# Persist login info
			g.cr_config.save()

			# Close the login window we are done
			self.close()

		print('Failed to login')

	def loadAssets(self):
		# Load hime over everything to the left of the login form
		self.hime_image = QLabel(self.container)
		self.hime_image.setContentsMargins(0, 0, 0, 0)
		self.hime_image.setAlignment(Qt.AlignTop)
		qpm = QPixmap('assets/log-in-hime@2x.png')
		# Images seem to already scaled down for hidpi screens
		# We need to scale twice to get rid of the original down scale, and then
		# once more to get to the size we actually want
		qpm = qpm.scaledToHeight(g.scale(g.scale(488)), Qt.SmoothTransformation)
		self.hime_image.setPixmap(qpm)
		self.hime_image.setFixedHeight(g.scale(488 + 32))
		self.hime_image.setFixedWidth(g.scale(186 + 5))
		self.hime_image.setStyleSheet("""
			QLabel {
		"""
		f"""
				margin-top: {g.scale(32)}px;
				margin-left: {g.scale(5)}px;
		"""
		"""
			}
		""")
		# Make image clickthrough
		self.hime_image.setAttribute(Qt.WA_TransparentForMouseEvents)

		# Load yuzu over everything to the bottom right of the login form
		self.yuzu_image = QLabel(self.container)
		qpm = QPixmap('assets/log-in-yuzu@2x.png')
		# Images seem to already scaled down for hidpi screens
		# We need to scale twice to get rid of the original down scale, and then
		# once more to get to the size we actually want
		qpm = qpm.scaledToHeight(g.scale(g.scale(108)), Qt.SmoothTransformation)
		self.yuzu_image.setPixmap(qpm)
		self.yuzu_image.setFixedHeight(g.scale(108 + 417))
		self.yuzu_image.setFixedWidth(g.scale(118 + 613))
		self.yuzu_image.setStyleSheet("""
			QLabel {
		"""
		f"""
				margin-top: {g.scale(417)}px;
				margin-left: {g.scale(613)}px;
		"""
		"""
			}
		""")
		# Make image clickthrough
		self.yuzu_image.setAttribute(Qt.WA_TransparentForMouseEvents)

	def setInputStyle(self, input: QLineEdit, color: str = '#ffffff', border_color: str = '#59595b'):
		input.setStyleSheet("""
			QLineEdit {
				background-color: #141519;
				border: none;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
		"""
		f"""
				color: {color};
				max-height: {g.scale(34)}px;
				border-bottom: {g.scale(2)}px solid {border_color};
				padding-top: {g.scale(4)}px;
				padding-bottom: {g.scale(2)}px;
		"""
		"""
			}
			QLineEdit:focus {
		"""
		f"""
				border-bottom: {g.scale(2)}px solid #f47521;
		"""
		"""
			}
		""")
