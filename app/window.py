from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import crunchyroll_api.watchlist as WatchlistClasses
import crunchyroll_api.series as SeriesClasses

from watchlist.widget import WatchList
from player.widget import Player
from utils.layout import addCloseButton, addMoveOnDrag

import global_vars.vars as g

class MainWindow(QMainWindow):
	can_drag: bool = True
	stacked_layout: QStackedLayout = None
	watchlist_widget: QWidget = None
	watchlist_layout: QVBoxLayout = None
	player_widget: QWidget = None
	player_layout: QVBoxLayout = None

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

		self.watchlist_widget = QWidget()
		self.watchlist_layout = QVBoxLayout(self.watchlist_widget)
		self.watchlist_layout.setContentsMargins(0, 0, 0, 0)
		self.watchlist_layout.setSpacing(0)

		self.player_widget = QWidget()
		self.player_layout = QVBoxLayout(self.player_widget)
		self.player_layout.setContentsMargins(0, 0, 0, 0)
		self.player_layout.setSpacing(0)
		# TODO: Remove temporary fixed size
		self.player_widget.setFixedSize(g.scale(1280), g.scale(720))

		self.stacked_layout = QStackedLayout(self.container)
		self.stacked_layout.addWidget(self.watchlist_widget)
		self.stacked_layout.addWidget(self.player_widget)

		# TODO: Figure out how to add this earlier and keep it on top of
		# everything
		addCloseButton(self)

		# Set default widget
		self.navigateToWatchList()

	def navigateToWatchList(self):
		play_episode = lambda title, series: self.navigateToPlayer(title, series)
		self.watchlist = WatchList(self.watchlist_layout, play_episode)

		self.stacked_layout.setCurrentIndex(0)

	def navigateToPlayer(self, title: WatchlistClasses.Data, series: SeriesClasses.Data):
		self.player = Player(self.player_layout, title, series)
		# self.player.registerEvents()

		self.stacked_layout.setCurrentIndex(1)
