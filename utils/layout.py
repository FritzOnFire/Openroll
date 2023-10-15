from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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
