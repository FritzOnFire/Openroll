import os
import json
from datetime import datetime

import global_vars.constants as gc
from utils.config import checkBaseDir
from crunchyroll_api import constants as c

class CRConfig:
	access_token: str = 'giKq5eY27ny3cqz'
	client_id: str = 'noaihdevm_6iyg0a8l0q:'

	refresh_token: str = None
	cookies: dict = None

	def __init__(self):
		# Check if Openroll exists in user's .config directory
		if checkBaseDir() == False or self.checkCRConfigFile() == False:
			self.save()
			return

		# Load the config file
		conf_file = open(gc.cr_config_file, 'r')
		config = json.loads(conf_file.read())
		conf_file.close()

		if 'access_token' in config:
			self.access_token = config['access_token']

		if 'client_id' in config:
			self.client_id = config['client_id']

		if 'refresh_token' in config:
			self.refresh_token = config['refresh_token']

		if 'cookies' in config:
			self.cookies = config['cookies']

	def checkCRConfigFile(self):
		return os.path.exists(gc.cr_config_file)

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(gc.config_dir)

		data = {
			'access_token': self.access_token,
			'client_id': self.client_id
		}

		if self.refresh_token != None:
			data['refresh_token'] = self.refresh_token

		if self.cookies != None:
			data['cookies'] = self.cookies

		# Create the config file
		conf_file = open(gc.cr_config_file, 'w')
		json_raw = json.dumps(data, indent=4)
		json_raw = json_raw.replace('    ', '\t')
		conf_file.write(json_raw)
		conf_file.close()

		# Set the permissions
		os.chmod(gc.cr_config_file, 0o600)
