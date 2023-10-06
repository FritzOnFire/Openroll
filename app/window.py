from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from player.widget import Player
from utils.layout import cleanLayout

class MainWindow(QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)

		# Set the size of the main window
		self.setGeometry(0, 0, 800, 600)

		# Center the window
		qtRectangle = self.frameGeometry()
		centerPoint = QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

		self.container = QWidget(self)
		self.setCentralWidget(self.container)
		self.container.setAttribute(Qt.WA_DontCreateNativeAncestors)
		self.container.setAttribute(Qt.WA_NativeWindow)

		self.top_layout = QBoxLayout(QBoxLayout.TopToBottom, self.container)

		# Set default widget
		self.navigateToPlayer()

	def navigateToPlayer(self):
		cleanLayout(self.top_layout)

		self.player = Player(self.top_layout, None, 'the-saints-magic-power-is-omnipotent')
		self.player.registerEvents()
