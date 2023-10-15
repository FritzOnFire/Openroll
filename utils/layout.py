from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import global_vars.vars as g

def cleanLayout(layout: QBoxLayout):
	for i in reversed(range(layout.count())):
		layout.itemAt(i).widget().setParent(None)

def addMoveOnDrag(window: QMainWindow):
	# Move window on drag
	window.dragPos = QPoint()
	def mousePressEvent(event):
		window.dragPos = event.globalPos()
	def mouseMoveEvent(event):
		if event.buttons() == Qt.LeftButton and window.can_drag:
			window.move(window.pos() + event.globalPos() - window.dragPos)
			window.dragPos = event.globalPos()
	window.mousePressEvent = mousePressEvent
	window.mouseMoveEvent = mouseMoveEvent

def addCloseButton(window: QMainWindow):
	window.close_button = QPushButton('×', window.container)

	setCloseButtonOffset(window)

	window.close_button.setFixedSize(21, 21)

	window.resizeEvent = lambda event: setCloseButtonOffset(window)

	window.close_button.clicked.connect(window.close)

def setCloseButtonOffset(window: QMainWindow):
	offset = window.frameGeometry().width() - g.scale(21 + 5)

	window.close_button.setStyleSheet("""
		QPushButton {
			color: #ffffff;
			border: none;
	"""
	f"""	font-size: {g.scale(20)}px;
			padding-bottom: {g.scale(1)}px;
			max-width: {g.scale(21)}px;
			min-width: {g.scale(21)}px;
			max-height: {g.scale(21)}px;
			min-height: {g.scale(21)}px;
			margin-top: {g.scale(5)}px;
			margin-left: {offset}px;
	"""
	"""
		}
		QPushButton:hover {
			background-color: #f47521;
		}
	""")

def underLineLabel(label: QLabel):
	f = label.font()
	f.setUnderline(True)
	label.setFont(f)

def removeUnderLineLabel(label: QLabel):
	f = label.font()
	f.setUnderline(False)
	label.setFont(f)

def makeInvisible(label: QLabel):
	label.setVisible(False)

def makeVisible(label: QLabel):
	label.setVisible(True)
