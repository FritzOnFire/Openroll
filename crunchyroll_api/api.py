import requests
from bs4 import BeautifulSoup

class CrunchyrollAPI:
	logged_in: bool = False

	def __init__(self):
		self.session = requests.Session()
		self.session.headers.update({
			'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0'
		})

	def login(self, username: str, password: str):
		"""
			Login to Crunchyroll
			:param username: Username or email
			:param password: Password
			:return: True if login was successful
		"""
		# Get the login page
		response = self.session.get('https://www.crunchyroll.com/login')
		# Get the login form
		soup = BeautifulSoup(response.text, 'html.parser')
		print(soup)
		form = soup.find('form', {'id': 'login_form'})
		# Get the login token
		token = form.find('input', {'name': 'login_form[_token]'})['value']
		# Login
		response = self.session.post('https://www.crunchyroll.com/login', data={
			'login_form[name]': username,
			'login_form[password]': password,
			'login_form[redirect_url]': '',
			'login_form[_token]': token
		})
		# Check if login was successful
		soup = BeautifulSoup(response.text, 'html.parser')
		if soup.find('form', {'id': 'login_form'}) is not None:
			return False
		self.logged_in = True
		return True

	def retriveToken(self):
		"""
			Retrieve the token
			:return: Token
		"""
		response = self.session.post('https://www.crunchyroll.com/auth/v1/token', data={
			'device_id': '0',
			'device_type': 'Chrome on Linux',
			'grant_type': 'etp_rt_cookie'
		})
		if response.ok == False:
			raise Exception('while getting token: ' + response.text)
		self.token = response.json()

	def getAccountID(self):
		"""
			Get the account ID
			:return: Account ID
		"""
		if self.token == None:
			try:
				self.retriveToken()
			except Exception as e:
				raise e

		return self.token['account_id']

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
