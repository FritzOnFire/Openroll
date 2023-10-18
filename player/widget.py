import mpv
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import crunchyroll_api.watchlist as WatchlistClasses
import crunchyroll_api.series as SeriesClasses

import global_vars.constants as gc
import global_vars.vars as g

from player.yt_dlp_config import YTDLPConfig
from player.mpv_config import MPVConfig
from player.playlist import Playlist

class Player:
	yt_dlp_config: YTDLPConfig = None
	mpv_config: MPVConfig = None
	player: mpv.MPV = None
	counter: int = 0

	def __init__(self, layout: QVBoxLayout, title: WatchlistClasses.Data, series: SeriesClasses.Data):
		self.yt_dlp_config = YTDLPConfig()
		self.mpv_config = MPVConfig()

		self.mpv_container = QWidget()

		height = min(layout.geometry().width() * 0.5625, layout.geometry().height() * 0.7)
		self.mpv_container.setFixedSize(layout.geometry().width(), int(height))

		self.player = mpv.MPV(
			wid=str(int(self.mpv_container.winId())),
			ytdl=True,
			log_handler=print,
			loglevel='warn',
			config_dir=gc.mpv_config_dir)

		self.playlist = Playlist(self.player, title, series)
		self.playlist.setPlaylist()
		self.playlist.setCurrentEpisode()

		seek_thread = threading.Thread(target=self.setLastPlayedPosition, args=(title.playhead,))
		seek_thread.start()

		layout.addWidget(self.mpv_container, 0, Qt.AlignTop)

		info_container = QWidget()
		info_container_layout = QVBoxLayout(info_container)
		info_container_layout.setContentsMargins(0, 0, 0, 0)
		info_container_layout.setSpacing(0)

		info_container_layout.addWidget(self.createInfoHeader(title, series), 0, Qt.AlignTop | Qt.AlignHCenter)

		layout.addWidget(info_container)

	def __del__(self):
		if self.player:
			self.player.terminate()

	def createInfoHeader(self, title: WatchlistClasses.Data, series: SeriesClasses.Data):
		header = QWidget()
		header_layout = QHBoxLayout(header)
		header_layout.setContentsMargins(0, 0, 0, 0)
		header_layout.setSpacing(0)

		info_label = QLabel(title.panel.episode_metadata.series_title, header)
		info_label.font().setPixelSize(g.scale(16))

		info_label.setStyleSheet("""
			QLabel {
				background-color: #141519;
				color: #ffffff;
				font-weight: 500;
				font-family: Lato,Helvetica Neue,helvetica,sans-serif;
			}
		""")

		header_layout.addWidget(info_label, 0, Qt.AlignLeft)

		return header

	def registerEvents(self):
		self.player.observe_property('time-pos', self.update)

	def update(self, name: str, value):
		self.counter += 1
		if self.counter % 50 != 0:
			return

		print('update')
		self.info_label.setText(str(value))
		self.info_container.update()

	def setLastPlayedPosition(self, position: int):
		self.player.wait_until_playing()
		self.player.seek(position)
