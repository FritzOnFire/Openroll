import threading
import requests

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import crunchyroll_api.watchlist as WatchlistClasses

class Tile:
	widget: QWidget = None
	layout: QVBoxLayout = None
	thumbnail: QLabel = None
	session: requests.Session = None
	title: WatchlistClasses.Data = None

	def __init__(self, title: WatchlistClasses.Data):
		self.session = requests.Session()
		self.title = title

		self.widget = QWidget()
		self.layout = QVBoxLayout(self.widget)

		self.widget.setStyleSheet("""
			QWidget {
				background-color: #000000;
				max-width: 240px;
				min-width: 240px;
				max-height: 249px;
				min-height: 249px;
			}
		""")

		# Add the thumbnail
		self.thumbnail = QLabel(self.widget)
		self.thumbnail.setStyleSheet("""
			QLabel {
				max-width: 240px;
				min-width: 240px;
				max-height: 135px;
				min-height: 135px;
			}
		""")
		self.thumbnail.setScaledContents(True)
		self.layout.addWidget(self.thumbnail)

		# Update thumbnail with the real one in a new thread
		thumbnail_thread = threading.Thread(target=self.updateThumbnail)
		thumbnail_thread.start()

		# Add the series title
		title_label = QLabel(title.panel.episode_metadata.series_title, self.widget)
		title_label.setStyleSheet("""
			QLabel {
				color: #ffffff;
				font-size: 16px;
				font-weight: 600;
				max-height: 48px;
				min-height: 24px;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")
		title_label.setWordWrap(True)
		self.layout.addWidget(title_label)

	def updateThumbnail(self):
		thumbnail_arr_arr = self.title.panel.images.thumbnail
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
		responce = self.session.get(thumbnail_url)
		if responce.ok == False:
			print('while downloading thumbnail: ' + responce.text)
			return

		qpm = QPixmap(240, 135)
		qpm.loadFromData(responce.content)
		# The following line cases a segfault :(
		# RuntimeError: wrapped C/C++ object of type QLabel has been deleted
		# self.thumbnail.setPixmap(qpm)
