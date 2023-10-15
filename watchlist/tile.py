import threading
import requests

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import QSvgWidget

import crunchyroll_api.watchlist as WatchlistClasses
import crunchyroll_api.series as SeriesClasses
import watchlist.constants as c

import global_vars.vars as g

from utils.layout import underLineLabel, removeUnderLineLabel, makeInvisible, makeVisible
from utils.thumbnail import getThumbnail

class Tile:
	widget: QWidget = None
	layout: QVBoxLayout = None
	thumbnail_widget: QWidget = None
	thumbnail: QLabel = None
	thumbnail_hover: QLabel = None
	session: requests.Session = None
	play_episode: callable = None

	thumbnail_thread: threading.Thread = None

	def __init__(self, title: WatchlistClasses.Data, series: SeriesClasses.Data, play_episode: callable):
		self.play_episode = play_episode
		self.session = requests.Session()

		self.widget = QWidget()
		self.widget.setFixedSize(g.scale(c.TILE_WIDTH), g.scale(c.TILE_HEIGHT))
		self.widget.setContentsMargins(0, 0, 0, 0)
		self.widget.setStyleSheet("""
			QWidget:hover {
				background-color: #141519;
			}
		""")

		# Call play_episode when the tile is clicked
		self.widget.mousePressEvent = lambda event: self.play_episode(title, series)

		self.layout = QVBoxLayout(self.widget)
		self.layout.setSpacing(0)
		m = g.scale(c.TILE_MARGIN)
		self.layout.setContentsMargins(m, m, m, m)

		self.createThumbnail(self.widget, title, series)
		self.layout.addWidget(self.thumbnail_widget, 0, Qt.AlignLeft)

		# Add the series title
		title_label = QLabel(self.widget)
		title_label.setContentsMargins(0, g.scale(12), 0, g.scale(4))
		title_label.setFixedWidth(g.scale(c.THUMB_WIDTH))
		title_label.setMaximumHeight(g.scale(60))
		title_label.setMinimumHeight(g.scale(24))
		font = title_label.font()
		font.setPixelSize(g.scale(16))
		font.setWeight(QFont.Weight.DemiBold)
		title_label.setFont(font)
		title_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				background-color: #00000000;
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
		media_type.setFixedHeight(g.scale(19))
		font = media_type.font()
		font.setPixelSize(g.scale(14))
		font.setWeight(QFont.Weight.DemiBold)
		media_type.setFont(font)
		media_type.setStyleSheet("""
			QLabel {
				color: #2abdbb;
				background-color: #00000000;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		footer_layout.addWidget(media_type)

		diamond = QLabel("◆", footer)
		diamond.setFixedHeight(g.scale(15))
		font = diamond.font()
		font.setPixelSize(g.scale(9))
		diamond.setFont(font)
		diamond.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				padding-left: 1px;
				padding-right: 1px;
			}
		""")
		diamond.setAlignment(Qt.AlignTop)
		footer_layout.addWidget(diamond)

		sub_dub = QLabel(title.panel.episode_metadata.subAndDubComment(), footer)
		sub_dub.setFixedHeight(g.scale(18))
		font = sub_dub.font()
		font.setPixelSize(g.scale(14))
		font.setWeight(QFont.Weight.Medium)
		sub_dub.setFont(font)
		sub_dub.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		footer_layout.addWidget(sub_dub, 1, Qt.AlignLeft)

		heart = QSvgWidget('./assets/heart.svg', footer)
		heart.setFixedSize(g.scale(24), g.scale(24))

		effect = QGraphicsColorizeEffect()
		effect.setColor(QColor('#a0a0a0'))
		effect.setStrength(1.0)
		heart.setGraphicsEffect(effect)

		footer_layout.addWidget(heart, 0, Qt.AlignRight)

		footer_layout.addSpacing(g.scale(8))

		trash_can = QSvgWidget('./assets/trash_can.svg', footer)
		trash_can.setFixedSize(g.scale(24), g.scale(24))

		effect = QGraphicsColorizeEffect()
		effect.setColor(QColor('#a0a0a0'))
		effect.setStrength(1.0)
		trash_can.setGraphicsEffect(effect)

		footer_layout.addWidget(trash_can, 0, Qt.AlignRight)

		return footer

	def createThumbnail(self, parent: QWidget, title: WatchlistClasses.Data, series: SeriesClasses.Data):
		self.thumbnail_widget = QWidget(parent)
		self.thumbnail_widget.setFixedSize(g.scale(c.THUMB_WIDTH), g.scale(c.THUMB_HEIGHT))
		self.thumbnail_widget.setStyleSheet("""
			QLabel {
				background-color: #323232;
			}
		""")

		# Create hover first as it needs to be behind the thumbnail
		self.thumbnail_hover = QLabel(self.thumbnail_widget)
		self.thumbnail_hover.setFixedSize(g.scale(c.THUMB_WIDTH), g.scale(c.THUMB_HEIGHT))
		self.thumbnail_hover.setStyleSheet("""
			QLabel {
				background-color: #323232;
			}
		""")
		self.thumbnail_hover.setScaledContents(True)

		self.createDurationOnThumbnail(title)

		self.thumbnail = QLabel(self.thumbnail_widget)
		self.thumbnail.setFixedSize(g.scale(c.THUMB_WIDTH), g.scale(c.THUMB_HEIGHT))
		self.thumbnail.setStyleSheet("""
			QLabel {
				background-color: #323232;
			}
		""")
		self.thumbnail.setScaledContents(True)

		# Make thumbnail invisible when mouse is over it
		self.widget.setMouseTracking(True)
		self.widget.enterEvent = lambda event: makeInvisible(self.thumbnail)
		self.widget.leaveEvent = lambda event: makeVisible(self.thumbnail)

		# Update thumbnails with the real ones in a new threads

		self.thumbnail_thread = threading.Thread(target=self.downloadThumbnail, args=(series, title))
		self.thumbnail_thread.start()

	def downloadThumbnail(self, series: SeriesClasses.Data,  title: WatchlistClasses.Data):
		thumbnail_url = series.thumbnailURL()
		if len(thumbnail_url) > 0:
			thumbnail_raw = getThumbnail(thumbnail_url)

			qpm = QPixmap()
			qpm.loadFromData(thumbnail_raw)
			self.thumbnail.setPixmap(qpm)

		thumbnail_url = title.thumbnailURL()
		if len(thumbnail_url) > 0:
			thumbnail_raw = getThumbnail(thumbnail_url)

			qpm = QPixmap()
			qpm.loadFromData(thumbnail_raw)
			self.thumbnail_hover.setPixmap(qpm)

	def createDurationOnThumbnail(self, title: WatchlistClasses.Data) -> QLabel:
		thumbnail_layout = QVBoxLayout(self.thumbnail_widget)
		thumbnail_layout.setContentsMargins(0, 0, 0, 0)
		thumbnail_layout.setSpacing(0)

		# Create the duration label
		duration_label = QLabel(title.durationComment(), self.thumbnail_widget)
		duration_label.setFixedHeight(g.scale(14 + 5))
		font = duration_label.font()
		font.setPixelSize(g.scale(14))
		font.setWeight(QFont.Weight.Medium)
		duration_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				background-color: rgba(0,0,0,60%);
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
		"""
		f"""
				margin-right: {g.scale(4)}px;
		"""
		"""
			}
		""")
		duration_label.setContentsMargins(g.scale(5), g.scale(3), g.scale(5), g.scale(3))

		thumbnail_layout.addWidget(duration_label, 1, Qt.AlignBottom | Qt.AlignRight)

		# Create progress bar
		progress_bar = QProgressBar(self.thumbnail_widget)
		progress_bar.setFixedSize(g.scale(c.THUMB_WIDTH), g.scale(4))
		progress_bar.setStyleSheet("""
			QProgressBar {
				background-color: rgba(0,0,0,60%);
				border: none;
			}
			QProgressBar::chunk {
				background-color: #f47521;
				border: none;
			}
		""")

		progress_bar.setRange(0, title.panel.episode_metadata.duration_ms)
		progress_bar.setValue(title.playhead * 1000)
		progress_bar.setTextVisible(False)

		# We still make the progress bar, as it is the easiest way to add the
		# space below the duration label on the thumbnail
		if title.playhead == 0:
			progress_bar.setStyleSheet("""
				QProgressBar {
					background-color: rgba(0,0,0,0%);
					border: none;
				}
			""")

		thumbnail_layout.addWidget(progress_bar, 0, Qt.AlignBottom | Qt.AlignLeft)

	def createEpisodeComment(self, parent: QWidget, title: WatchlistClasses.Data) -> QLabel:
		comment_label = QLabel(title.episodeComment(), parent)
		comment_label.setFixedHeight(g.scale(18))
		font = comment_label.font()
		font.setPixelSize(g.scale(14))
		font.setWeight(QFont.Weight.Medium)
		comment_label.setStyleSheet("""
			QLabel {
				color: #a0a0a0;
				background-color: #00000000;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		return comment_label
