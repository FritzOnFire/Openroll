import os
import json
from datetime import datetime

from utils.config import checkBaseDir
from crunchyroll_api import constants as c

class CRConfig:
	access_token: str = 'giKq5eY27ny3cqz'
	client_id: str = 'noaihdevm_6iyg0a8l0q'

	auth_key: str = None
	auth_expires: datetime = None
	user_id: int = None
	etp_guid: str = None
	cookie: dict = None

	def __init__(self):
		# Check if Openroll exists in user's .config directory
		if checkBaseDir() == False or self.checkCRConfigFile() == False:
			self.save()
			return

		# Load the config file
		conf_file = open(os.path.expanduser('~/.config/openroll/cr_config.json'), 'r')
		config = json.loads(conf_file.read())
		conf_file.close()

		if 'access_token' in config:
			self.access_token = config['access_token']

		if 'client_id' in config:
			self.client_id = config['client_id']

		if 'auth_key' in config:
			self.auth_key = config['auth_key']

		if 'auth_expires' in config:
			self.auth_expires = datetime.strptime(config['auth_expires'], c.EXPIRE_DATE_FORMAT)

		if 'user_id' in config:
			self.user_id = config['user_id']

		if 'etp_guid' in config:
			self.etp_guid = config['etp_guid']

		if 'cookie' in config:
			self.cookie = config['cookie']

	def checkCRConfigFile(self):
		return os.path.exists(os.path.expanduser('~/.config/openroll/cr_config.json'))

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(os.path.expanduser('~/.config/openroll'))

		data = {
			'access_token': self.access_token,
			'client_id': self.client_id
		}

		if self.auth_key != None:
			data['auth_key'] = self.auth_key

		if self.auth_expires != None:
			data['auth_expires'] = self.auth_expires.strftime(c.EXPIRE_DATE_FORMAT)

		if self.user_id != None:
			data['user_id'] = self.user_id

		if self.etp_guid != None:
			data['etp_guid'] = self.etp_guid

		if self.cookie != None:
			data['cookie'] = self.cookie

		# Create the config file
		conf_file = open(os.path.expanduser('~/.config/openroll/cr_config.json'), 'w')
		conf_file.write(json.dumps(data, indent=4))
		conf_file.close()

		# Set the permissions
		os.chmod(os.path.expanduser('~/.config/openroll/cr_config.json'), 0o600)
