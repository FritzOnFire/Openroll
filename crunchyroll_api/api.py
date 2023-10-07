import requests
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

		print(json)

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

	def retriveWatchList(self):
		"""
			Retrieve the watch list
			:return: List of anime
		"""

		response = self.session.get(f'https://www.crunchyroll.com/content/v2/discover/{self.config.etp_guid}/watchlist?order=desc&n=100&locale=en-US')
		if response.ok == False:
			raise Exception('while getting watch list: ' + response.text)
		return response.json()
