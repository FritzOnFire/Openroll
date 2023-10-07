import os
import uuid
import json

from utils.config import checkBaseDir

class Config:
	# Just set this to a random UUID every time the app starts
	device_id: str = uuid.uuid4().hex

	# Set this to True if you want to steal from Crunchyroll
	# But please do consider supporting them if you can
	i_am_a_pirate_and_want_to_steal_from_crunchyroll: bool = False

	def __init__(self):
		if checkBaseDir() == False or self.checkConfigFile() == False:
			self.save()
			return

		# Load config
		conf_file = open(os.path.expanduser('~/.config/openroll/openroll.json'), 'r')
		config = json.loads(conf_file.read())
		conf_file.close()

		if config['i_am_a_pirate_and_want_to_steal_from_crunchyroll'] != None:
			self.i_am_a_pirate_and_want_to_steal_from_crunchyroll = config['i_am_a_pirate_and_want_to_steal_from_crunchyroll']

	def checkConfigFile(self):
		return os.path.exists(os.path.expanduser('~/.config/openroll/openroll.json'))

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(os.path.expanduser('~/.config/openroll'))

		data = {
			'i_am_a_pirate_and_want_to_steal_from_crunchyroll': self.i_am_a_pirate_and_want_to_steal_from_crunchyroll
		}

		# Create the config file
		conf_file = open(os.path.expanduser('~/.config/openroll/openroll.json'), 'w')
		conf_file.write(json.dumps(data, indent=4))
		conf_file.close()

		# Set the permissions
		os.chmod(os.path.expanduser('~/.config/openroll/openroll.json'), 0o600)

	def isAddsActive(self):
		return self.i_am_a_pirate_and_want_to_steal_from_crunchyroll
