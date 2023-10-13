from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import crunchyroll_api.constants as c
import crunchyroll_api.watchlist as WatchlistClasses

import global_vars.vars as g

from watchlist.tile import Tile

WATCHLIST_TITLE_PER_ROW = 4

class WatchList:
	tiles: list[Tile] = []

	def __init__(self, layout: QVBoxLayout):
		layout.addWidget(self.createTitleWidget(), 0, Qt.AlignHCenter | Qt.AlignTop)
		layout.addStretch(1)

		layout.addWidget(self.createListWidget(), 0, Qt.AlignHCenter | Qt.AlignTop)
		layout.addStretch(1)

	def createTitleWidget(self):
		title_widget = QWidget()
		title_layout = QHBoxLayout(title_widget)

		# Add list.svg in front of the title
		title_icon = QLabel(title_widget)
		title_icon.setPixmap(QPixmap('./assets/list.svg'))
		title_icon.setScaledContents(True)
		title_icon.setMaximumSize(32, 32)
		title_icon.setMinimumSize(32, 32)

		effect = QGraphicsColorizeEffect()
		effect.setColor(QColor('#ffffff'))
		effect.setStrength(1.0)
		title_icon.setGraphicsEffect(effect)

		title_layout.addWidget(title_icon)

		self.title_label = QLabel('My Lists')
		self.title_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				font-size: 28px;
				font-weight: 500;
				max-height: 36px;
				min-height: 36px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		title_layout.addWidget(self.title_label)
		title_layout.addStretch(1)
		return title_widget

	def createListWidget(self) -> QWidget:
		try:
			watchlist = g.crunchyroll.retriveWatchlist()
		except Exception as e:
			print(e)
			return

		list_widget = QWidget()
		list_layout = QVBoxLayout(list_widget)

		num_rows = int(watchlist.total / c.WATCHLIST_TITLE_PER_ROW)
		# num_rows = 1
		last_row = watchlist.total % c.WATCHLIST_TITLE_PER_ROW

		for i in range(num_rows):
			start = i * c.WATCHLIST_TITLE_PER_ROW
			end = start + c.WATCHLIST_TITLE_PER_ROW
			list_layout.addWidget(self.createRowWidget(watchlist.data[start:end]), 0, Qt.AlignHCenter | Qt.AlignTop)

		return list_widget

	def createRowWidget(self, titles: list[WatchlistClasses.Data]) -> QWidget:
		row_widget = QWidget()
		row_layout = QHBoxLayout(row_widget)

		for title in titles:
			# Keep tiles around to avoid garbage collection
			tile = Tile(title)
			self.tiles.append(tile)
			row_layout.addWidget(tile.widget, 0, Qt.AlignLeft)

		return row_widget
