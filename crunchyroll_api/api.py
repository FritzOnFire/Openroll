import requests
import base64
from datetime import datetime

import crunchyroll_api.constants as c
from crunchyroll_api.config import CRConfig

class CrunchyrollAPI:
	device_id: str = None
	config: CRConfig = None
	session: requests.Session = None

	logged_in: bool = False
	session_id: int = None
	premium_user: bool = None

	def __init__(self, device_id: str, config: CRConfig):
		self.device_id = device_id
		self.config = config
		self.session = requests.Session()

		# Setting the user agent feels wrong, but I can's seem to find the `api`
		# endpoint for watchlist, so I guess we are stuck doing it like this
		self.session.headers.update({
			'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
		})

		# Experamental
		if self.config.cookie != None:
			self.session.cookies.update(self.config.cookie)

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

	def login(self, username: str, password: str):
		"""
			Login to Crunchyroll
			:param username: Username or email
			:param password: Password
		"""
		try:
			session_id = self.getSessionID()
		except Exception as e:
			raise Exception("while getting session id: " + str(e))

		response = self.session.post(c.LOGIN_URL, data={
			'account': username,
			'password': password,
			'session_id': session_id
		})
		if response.ok == False or response.json()['error'] == True:
			raise Exception('while logging in: ' + response.text)
		self.logged_in = True

		json = response.json()
		self.parseAuth(json['data'])
		self.parseUser(json['data']['user'])

		# Not sure if I need this... or if this can even be used
		self.config.cookie = self.session.cookies.get_dict()

	def parseAuth(self, response):
		self.config.auth_key = response['auth']
		if response['expires'].endswith(':00'):
			response['expires'] = response['expires'][:-3] + '00'
		self.config.auth_expires = datetime.strptime(response['expires'], c.EXPIRE_DATE_FORMAT)

	def parseUser(self, user):
		self.premium_user = user['premium'].find('anime') > 0
		self.config.user_id = user['user_id']
		self.config.etp_guid = user['etp_guid']

	def getToken(self):
		"""
			Get a new token
			:return: Token
		"""
		self.session.cookies.clear()
		self.session.cookies.set('etp_rt', self.config.cookie['etp_rt'])
		self.session.cookies.set('__cf_bm', self.config.cookie['__cf_bm'])

		response = self.session.post(c.TOKEN_URL, data={
			'device_id': self.device_id,
			'device_type': 'com.crunchyroll.static',
			'grant_type': 'etp_rt_cookie'
		}, headers={
			'authorization': 'Basic ' + base64.b64encode(f'{self.config.client_id}:'.encode()).decode(),
		})
		if response.ok == False:
			raise Exception('while hitting token endpoint: ' + response.text)
		return response.json()['access_token']

	def retriveWatchList(self):
		"""
			Retrieve the watch list
			:return: List of anime
		"""

		try:
			token = self.getToken()
		except Exception as e:
			raise Exception("while getting token: " + str(e))

		response = self.session.get(f'https://www.crunchyroll.com/content/v2/discover/{self.config.etp_guid}/watchlist?order=desc&n=100&locale=en-US', headers={
			'authorization': f'Bearer {token}'
		})
		if response.ok == False:
			raise Exception('while getting watch list: ' + response.text)
		return response.json()
