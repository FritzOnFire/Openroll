from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

def cleanLayout(layout: QBoxLayout):
	for i in reversed(range(layout.count())):
		layout.itemAt(i).widget().setParent(None)

def addCloseButton(window: QMainWindow):
	window.close_button = QPushButton('×', window.container)

	offset = window.frameGeometry().width() - 21 - 5

	window.close_button.setStyleSheet("""
		QPushButton {
			color: #ffffff;
			font-size: 20px;
			border: none;
			padding-bottom: 1px;
			max-width: 21px;
			min-width: 21px;
			max-height: 21px;
			min-height: 21px;
			margin-top: 5px;
	"""
	f"		margin-left: {offset}px;"
	"""
		}
		QPushButton:hover {
			background-color: #f47521;
		}
	""")
	window.close_button.clicked.connect(window.close)

	# Disable can_drag when hovering over the close button
	def enterEvent(event):
		window.can_drag = False
	def leaveEvent(event):
		window.can_drag = True
	window.close_button.enterEvent = enterEvent
	window.close_button.leaveEvent = leaveEvent

	window.setWindowFlag(Qt.FramelessWindowHint)
