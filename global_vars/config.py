import os
import uuid
import json

import global_vars.constants as c

from utils.config import checkBaseDir

class Config:
	# Just set this to a random UUID every time the app starts
	device_id: str = uuid.uuid4().hex

	# Set this to True if you want to steal from Crunchyroll
	# But please do consider supporting them if you can
	i_am_a_pirate_and_want_to_steal_from_crunchyroll: bool = False

	disable_scale_factor: bool = False

	def __init__(self):
		if checkBaseDir() == False or self.checkConfigFile() == False:
			self.save()
			return

		# Load config
		conf_file = open(c.config_file, 'r')
		config = json.loads(conf_file.read())
		conf_file.close()

		if 'i_am_a_pirate_and_want_to_steal_from_crunchyroll' in config:
			self.i_am_a_pirate_and_want_to_steal_from_crunchyroll = config['i_am_a_pirate_and_want_to_steal_from_crunchyroll']

		if 'disable_scale_factor' in config:
			self.disable_scale_factor = config['disable_scale_factor']

	def checkConfigFile(self):
		return os.path.exists(c.config_file)

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(c.config_dir)

		data = {
			'i_am_a_pirate_and_want_to_steal_from_crunchyroll': self.i_am_a_pirate_and_want_to_steal_from_crunchyroll,
			'disable_scale_factor': self.disable_scale_factor
		}

		# Create the config file
		conf_file = open(c.config_file, 'w')
		conf_file.write(json.dumps(data, indent=4))
		conf_file.close()

		# Set the permissions
		os.chmod(c.config_file, 0o600)

	def isAddsActive(self):
		return self.i_am_a_pirate_and_want_to_steal_from_crunchyroll
