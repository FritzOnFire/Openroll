from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from watchlist.widget import WatchList
from player.widget import Player
from utils.layout import cleanLayout
from utils.layout import addCloseButton, addMoveOnDrag

import global_vars.vars as g

class MainWindow(QMainWindow):
	can_drag: bool = True

	def __init__(self, parent=None):
		super().__init__(parent)

		# Set the size of the main window
		self.setGeometry(0, 0, g.scale(1280), g.scale(720))

		self.setWindowTitle('Openroll')
		self.setWindowFlag(Qt.FramelessWindowHint)

		addMoveOnDrag(self)

		# Center the window
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		self.setStyleSheet("""
			QMainWindow {
				background-color: #000000;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")

		self.container = QWidget(self)
		self.container.setContentsMargins(0, 0, 0, 0)
		self.setCentralWidget(self.container)

		self.top_layout = QVBoxLayout(self.container)
		self.top_layout.setSpacing(0)
		self.top_layout.setContentsMargins(0, 0, 0, 0)

		addCloseButton(self)

		# Set default widget
		self.navigateToWatchList()

	def navigateToWatchList(self):
		cleanLayout(self.top_layout)

		self.watchlist = WatchList(self.top_layout)

	def navigateToPlayer(self):
		cleanLayout(self.top_layout)

		self.player = Player(self.top_layout, None, 'the-saints-magic-power-is-omnipotent')
		self.player.registerEvents()
