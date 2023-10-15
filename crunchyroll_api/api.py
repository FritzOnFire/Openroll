import requests
import base64
import json

import crunchyroll_api.constants as c
from crunchyroll_api.config import CRConfig
from crunchyroll_api.watchlist import WatchlistResponse
from crunchyroll_api.series import SeriesResponse

class CrunchyrollAPI:
	device_id: str = None
	config: CRConfig = None
	session: requests.Session = None
	session_id: str = None

	logged_in: bool = False
	premium_user: bool = None
	account_id: str = None
	access_token: str = None

	def __init__(self, device_id: str, config: CRConfig):
		self.device_id = device_id
		self.config = config
		self.session = requests.Session()

		# Setting the user agent feels wrong, but I can's seem to find the `api`
		# endpoint for watchlist, so I guess we are stuck doing it like this
		self.session.headers.update({
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0'
		})

		# Set cookies if we have any
		if self.config.cookies != None:
			self.session.cookies.update(self.config.cookies)

	def login(self, username: str, password: str):
		"""
			Login to Crunchyroll
			:param username: Username or email
			:param password: Password
		"""
		try:
			token = self.getToken(username, password)
		except Exception as e:
			raise Exception("while getting token: " + str(e))

		self.parseAuth(token)
		self.parseUser(token)
		self.logged_in = True

		# Persist cookies
		self.config.cookies = self.session.cookies.get_dict()

	def parseAuth(self, token):
		self.access_token = token['access_token']
		self.config.refresh_token = token['refresh_token']

	def parseUser(self, token):
		# Pretty sure if you have offile_access you are premium
		self.premium_user = token['scope'].find('offline_access') > 0
		self.account_id = token['account_id']

	def getToken(self, username: str, password: str):
		headers = {
			'authorization': 'Basic ' + 'aHJobzlxM2F3dnNrMjJ1LXRzNWE6cHROOURteXRBU2Z6QjZvbXVsSzh6cUxzYTczVE1TY1k=',
			'content-type': 'application/x-www-form-urlencoded',
			'connection': 'keep-alive',
			'accept-encoding': 'gzip, deflate, br'
		}
		response = self.session.post(c.TOKEN_URL, data={
			'username': username,
			'password': password,
			'grant_type': 'password',
			'scope': 'offline_access'
		}, headers=headers)
		if response.ok == False:
			raise Exception('while hitting token endpoint: ' + response.text[:100])
		return response.json()

	def getTokenViaETP(self, etp_rt_cookie: str):
		"""
			Get a new token
			:return: Token
		"""
		self.session.cookies.set('etp_rt', etp_rt_cookie)

		headers = {
			'authorization': 'Basic ' + base64.b64encode(self.config.client_id.encode()).decode(),
			'content-type': 'application/x-www-form-urlencoded',
			'accept': 'application/json'
		}
		response = self.session.post(c.TOKEN_URL, data={
			'grant_type': 'etp_rt_cookie',
			'scope': 'offline_access'
		}, headers=headers)
		if response.ok == False:
			raise Exception('while hitting token endpoint: ' + response.text)
		return response.json()

	def getSessionID(self):
		if self.session_id != None:
			return self.session_id

		response = self.session.get(c.SESSION_URL, params={
			'device_id': self.device_id,
			'device_type': 'com.crunchyroll.static',
			'access_token': self.config.access_token
		})
		if response.ok == False or response.json()['error'] == True:
			raise Exception('while hitting session endpoint: ' + response.text)

		self.session_id = response.json()['data']['session_id']
		return self.session_id

	def retriveWatchlist(self) -> WatchlistResponse:
		"""
			Retrieve the watch list
			:return: List of anime
		"""
		# Load example responce
		example_file = open('crunchyroll_api/watchlist_example.json', 'r')
		response = json.loads(example_file.read())
		example_file.close()

		return WatchlistResponse(response)

		response = self.session.get(f'https://www.crunchyroll.com/content/v2/discover/{self.account_id}/watchlist?order=desc&n=100&locale=en-US', headers={
			'authorization': f'Bearer {self.access_token}'
		})
		if response.ok == False:
			raise Exception('while getting watch list: ' + response.text)
		return response.json()

	def retrieveSeriesFromWatchlist(self, watchlist: WatchlistResponse) -> SeriesResponse:
		# Load example responce
		example_file = open('crunchyroll_api/series_example.json', 'r')
		response = json.loads(example_file.read())
		example_file.close()

		return SeriesResponse(response)

		series_ids = ','.join([str(title.panel.episode_metadata.series_id) for title in watchlist.data])

		response = self.session.get(f'https://www.crunchyroll.com/content/v2/cms/objects/{series_ids}?ratings=true&preferred_audio_language=ja-JP&locale=en-US', headers={
			'authorization': f'Bearer {self.access_token}'
		})
		if response.ok == False:
			raise Exception('while getting series list: ' + response.text)
		return response.json()
