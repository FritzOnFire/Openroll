import mpv

import crunchyroll_api.watchlist as WatchlistClasses
import crunchyroll_api.series as SeriesClasses

class Playlist:
	player: mpv.MPV = None
	title: WatchlistClasses.Data = None
	series: SeriesClasses.Data = None

	def __init__(self, player: mpv.MPV, title: WatchlistClasses.Data, series: SeriesClasses.Data):
		self.player = player
		self.title = title
		self.series = series

	def setPlaylist(self):
		length = len(self.player.playlist)
		for i in range(length):
			self.player.playlist_remove(0)
		self.player.playlist_append(self.title.episodeURL())

	def setCurrentEpisode(self):
		self.player.playlist_pos = 0
