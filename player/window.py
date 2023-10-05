import mpv

from PyQt5.QtWidgets import *

from player.playlist import Playlist

class Player:
	player = None
	counter = 0

	def __init__(self, layout, crunchyroll, showName):
		self.info_container = QWidget()
		self.info_label = QLabel('Hello World', self.info_container)

		self.mpv_container = QWidget()
		self.player = mpv.MPV(
			wid=str(int(self.mpv_container.winId())),
			vo='x11', # You may not need this
			ytdl=True)

		self.playlist = Playlist(self.player, crunchyroll)
		self.playlist.setPlaylist(showName)
		self.playlist.setCurrentEpisode()

		layout.addWidget(self.info_container)
		layout.addWidget(self.mpv_container)

	def __del__(self):
		if self.player:
			self.player.terminate()

	def registerEvents(self):
		self.player.observe_property('time-pos', self.update)

	def update(self, name, value):
		self.counter += 1
		if self.counter % 50 != 0:
			return

		print('update')
		self.info_label.setText(str(value))
		self.info_container.update()
