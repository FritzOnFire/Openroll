class Playlist:
	def __init__(self, player, crunchyroll):
		self.player = player
		self.crunchyroll = crunchyroll

	def setPlaylist(self, showName):
		length = len(self.player.playlist)
		for i in range(length):
			self.player.playlist_remove(0)
		self.player.playlist_append('https://www.crunchyroll.com/watch/G31UXWQ47/the-trading-company')

	def setCurrentEpisode(self):
		self.player.playlist_pos = 0
