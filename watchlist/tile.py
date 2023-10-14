import threading
import requests

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import crunchyroll_api.watchlist as WatchlistClasses
import watchlist.constants as c

from utils.layout import underLineLabel, removeUnderLineLabel

class Tile:
	widget: QWidget = None
	layout: QVBoxLayout = None
	thumbnail_widget: QWidget = None
	thumbnail: QLabel = None
	session: requests.Session = None

	thumbnail_thread: threading.Thread = None

	def __init__(self, title: WatchlistClasses.Data):
		self.session = requests.Session()

		self.widget = QWidget()
		self.widget.setFixedSize(c.TILE_WIDTH, c.TILE_HEIGHT)
		self.widget.setContentsMargins(0, 0, 0, 0)
		self.widget.setStyleSheet("""
			QWidget:hover {
				background-color: #141519;
			}
		""")

		self.layout = QVBoxLayout(self.widget)
		self.layout.setSpacing(0)
		self.layout.setContentsMargins(c.TILE_MARGIN, c.TILE_MARGIN, c.TILE_MARGIN, c.TILE_MARGIN)

		self.createThumbnail(self.widget, title)
		self.layout.addWidget(self.thumbnail, 0, Qt.AlignLeft)

		# Add the series title
		title_label = QLabel(self.widget)
		title_label.setContentsMargins(0, 12, 0, 4)
		title_label.setFixedWidth(c.THUMB_WIDTH)
		title_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				background-color: #00000000;
				font-size: 16px;
				font-weight: 600;
				max-height: 60px;
				min-height: 24px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		title_label.setAlignment(Qt.AlignTop)
		title_label.setWordWrap(True)
		elidedText = QFontMetrics(title_label.font()).elidedText(title.panel.episode_metadata.series_title, Qt.ElideRight, int(title_label.width()*1.75))
		title_label.setText(elidedText)

		title_label.setMouseTracking(True)
		title_label.enterEvent = lambda event: underLineLabel(title_label)
		title_label.leaveEvent = lambda event: removeUnderLineLabel(title_label)

		self.layout.addWidget(title_label)

		comment = self.createEpisodeComment(self.widget, title)
		self.layout.addWidget(comment)

		self.layout.addWidget(self.createFooter(self.widget, title), 1, Qt.AlignBottom)

	def createFooter(self, parent: QWidget, title: WatchlistClasses.Data) -> QWidget:
		footer = QWidget(parent)
		footer.setContentsMargins(0, 0, 0, 0)
		footer.setStyleSheet("""
			QWidget {
				background-color: #00000000;
			}
		""")

		footer_layout = QHBoxLayout(footer)
		footer_layout.setContentsMargins(0, 0, 0, 0)
		footer_layout.setSpacing(0)

		media_type = QLabel("Series", footer)
		media_type.setStyleSheet("""
			QLabel {
				color: #2abdbb;
				background-color: #00000000;
				font-size: 14px;
				font-weight: 600;
				max-height: 19px;
				min-height: 19px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		footer_layout.addWidget(media_type)

		diamond = QLabel("◆", footer)
		diamond.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				font-size: 9px;
				max-height: 15px;
				min-height: 15px;
				padding-left: 1px;
				padding-right: 1px;
			}
		""")
		diamond.setAlignment(Qt.AlignTop)
		footer_layout.addWidget(diamond)

		sub_dub = QLabel(title.panel.episode_metadata.subAndDubComment(), footer)
		sub_dub.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				font-size: 14px;
				font-weight: 500;
				max-height: 18px;
				min-height: 18px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		footer_layout.addWidget(sub_dub, 1, Qt.AlignLeft)

		heart = QLabel(footer)
		heart.setPixmap(QPixmap('./assets/heart.svg'))
		heart.setScaledContents(True)
		heart.setMaximumSize(32, 24)
		heart.setMinimumSize(32, 24)

		effect = QGraphicsColorizeEffect()
		effect.setColor(QColor('#ffffff'))
		effect.setStrength(1.0)
		heart.setGraphicsEffect(effect)

		heart.setStyleSheet("""
			QLabel {
				margin-right: 8px;
			}
		""")

		footer_layout.addWidget(heart, 0, Qt.AlignRight)

		trash_can = QLabel(footer)
		trash_can.setPixmap(QPixmap('./assets/trash_can.svg'))
		trash_can.setScaledContents(True)
		trash_can.setMaximumSize(24, 24)
		trash_can.setMinimumSize(24, 24)

		effect = QGraphicsColorizeEffect()
		effect.setColor(QColor('#ffffff'))
		effect.setStrength(1.0)
		trash_can.setGraphicsEffect(effect)

		footer_layout.addWidget(trash_can, 0, Qt.AlignRight)

		return footer

	def createThumbnail(self, parent: QWidget, title: WatchlistClasses.Data):
		self.thumbnail = QLabel(parent)
		self.thumbnail.setFixedSize(c.THUMB_WIDTH, c.THUMB_HEIGHT)
		self.thumbnail.setStyleSheet("""
			QLabel {
				max-width: 240px;
				min-width: 240px;
				max-height: 135px;
				min-height: 135px;
				background-color: #323232;
			}
		""")
		self.thumbnail.setScaledContents(True)

		# Update thumbnail with the real one in a new thread
		self.thumbnail_thread = threading.Thread(target=self.downloadThumbnail, args=(title,))
		self.thumbnail_thread.start()

	def downloadThumbnail(self, title: WatchlistClasses.Data):
		thumbnail_arr_arr = title.panel.images.thumbnail
		thumbnail_arr = []
		if len(thumbnail_arr_arr) == 0:
			return # Nothing to do

		thumbnail_arr = thumbnail_arr_arr[0]
		if len(thumbnail_arr) == 0:
			return # Nothing to do

		thumbnail_url = thumbnail_arr[0].source
		if thumbnail_url == None:
			return # Nothing to do

		# Download the thumbnail
		session = requests.Session()
		responce = session.get(thumbnail_url)
		if responce.ok == False:
			print('while downloading thumbnail: ' + responce.text)
			return

		qpm = QPixmap()
		qpm.loadFromData(responce.content)
		self.thumbnail.setPixmap(qpm)

	def createEpisodeComment(self, parent: QWidget, title: WatchlistClasses.Data) -> QLabel:
		comment_label = QLabel(title.episodeComment(), parent)
		comment_label.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				font-size: 14px;
				font-weight: 500;
				max-height: 18px;
				min-height: 18px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		return comment_label
