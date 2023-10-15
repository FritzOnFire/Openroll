from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import crunchyroll_api.watchlist as WatchlistClasses
import crunchyroll_api.series as SeriesClasses

import global_vars.vars as g

from watchlist.tile import Tile
import watchlist.constants as c

WATCHLIST_TITLE_PER_ROW = 4

class WatchList:
	tiles: list[Tile] = []

	def __init__(self, layout: QVBoxLayout):
		layout.addWidget(self.createTitleWidget(), 0, Qt.AlignHCenter | Qt.AlignTop)

		layout.addWidget(self.createListWidget(), 1, Qt.AlignTop)

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
		return title_widget

	def createListWidget(self) -> QScrollArea:
		try:
			watchlist = g.crunchyroll.retriveWatchlist()
		except Exception as e:
			print(e)
			return

		try:
			series = g.crunchyroll.retrieveSeriesFromWatchlist(watchlist)
		except Exception as e:
			print(e)
			return

		list_widget = QWidget()
		list_widget.setContentsMargins(0, 0, 0, 0)
		list_widget.setStyleSheet("""
			QWidget {
				background-color: #000000;
			}
		""")

		list_layout = QVBoxLayout(list_widget)
		list_layout.setContentsMargins(0, 0, 0, 0)
		list_layout.setSpacing(c.TILE_GAP)

		num_rows = int(watchlist.total / WATCHLIST_TITLE_PER_ROW)
		# num_rows = 1
		last_row = watchlist.total % WATCHLIST_TITLE_PER_ROW

		for i in range(num_rows):
			start = i * WATCHLIST_TITLE_PER_ROW
			end = start + WATCHLIST_TITLE_PER_ROW
			list_layout.addWidget(self.createRowWidget(watchlist.data[start:end], series), 0, Qt.AlignTop)

		scroll = QScrollArea()
		scroll.setWidgetResizable(True)
		scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		policy = scroll.sizePolicy()
		policy.setVerticalStretch(1)
		policy.setHorizontalStretch(1)

		scroll.sizeHint = lambda: QSize(list_widget.size())

		scroll.setStyleSheet("""
			QScrollArea {
				background-color: #000000;
			}
			QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical
			{
				background: none;
				border: none;
			}
			QScrollBar:vertical {
				width: 8px;
				margin-right: 2px;
				background-color: #141519;
				border-radius: 3px;
			}
			QScrollBar::handle:vertical {
				min-height: 10px;
				background-color: #f47521;
				border-radius: 3px;
			}
		""")

		scroll.setWidget(list_widget)
		return scroll

	def createRowWidget(self, titles: list[WatchlistClasses.Data], series: SeriesClasses.SeriesResponse) -> QWidget:
		row_widget = QWidget()
		row_widget.setContentsMargins(0, 0, 0, 0)

		row_layout = QHBoxLayout(row_widget)
		row_layout.setContentsMargins(0, 0, 0, 0)
		row_layout.setSpacing(c.TILE_GAP)

		row_layout.addStretch(1)

		for title in titles:
			s = series.dataDict[title.panel.episode_metadata.series_id]

			# Keep tiles around to avoid garbage collection
			tile = Tile(title, s)
			self.tiles.append(tile)
			row_layout.addWidget(tile.widget, 0, Qt.AlignLeft)

		row_layout.addStretch(1)

		return row_widget
