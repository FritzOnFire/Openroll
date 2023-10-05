#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from player.window import Player

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

app = QApplication(sys.argv)

# This is necessary since PyQT stomps over the locale settings needed by libmpv.
# This needs to happen after importing PyQT before creating the first mpv.MPV
# instance.

import locale
locale.setlocale(locale.LC_NUMERIC, 'C')
win = MainWindow()

player = Player(win.top_layout, None, 'the-saints-magic-power-is-omnipotent')
player.registerEvents()

win.show()
sys.exit(app.exec_())
