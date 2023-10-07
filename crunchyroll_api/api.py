import requests
from datetime import datetime

import crunchyroll_api.constants as c

class CrunchyrollAPI:
	logged_in: bool = False
	session_id: int = None
	premium_user: bool = None
	auth_key: str = None
	auth_expires: datetime = None

	# There needs to be a way to scrape this from some site
	access_token: str = 'giKq5eY27ny3cqz'

	def __init__(self, device_id: str):
		self.device_id = device_id
		self.session = requests.Session()

	def getSessionID(self):
		if self.session_id != None:
			return self.session_id

		response = self.session.get(c.SESSION_URL, params={
			'device_id': self.device_id,
			'device_type': 'com.crunchyroll.static',
			'access_token': self.access_token
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

		self.parseAuth(response.json()['data'])
		self.parseUser(response.json()['data']['user'])

	def parseAuth(self, response):
		self.auth_key = response['auth']
		if response['expires'].endswith(':00'):
			response['expires'] = response['expires'][:-3] + '00'
		self.auth_expires = datetime.strptime(response['expires'], '%y-%m-%dT%H:%M:%S%z')

	def parseUser(self, user):
		self.premium_user = user['premium'].find('anime') > 0
		self.user_id = user['user_id']

	def retriveWatchList(self):
		"""
			Retrieve the watch list
			:return: List of anime
		"""

		try:
			id = self.getAccountID()
		except Exception as e:
			raise Exception("while getting account id: " + str(e))

		response = self.session.get(f'https://www.crunchyroll.com/content/v2/discover/{id}/watchlist?order=desc&n=100&locale=en-US')
		if response.ok == False:
			raise Exception('while getting watch list: ' + response.text)
		return response.json()
