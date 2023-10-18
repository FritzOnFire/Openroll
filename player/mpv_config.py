import os
import configparser

from global_vars.constants import config_dir, mpv_config_dir, yt_dlp_config_dir

from utils.config import checkBaseDir

class MPVConfig:
	cache: str = 'yes'
	demuxer_max_bytes: str = '5000M'
	demuxer_max_back_bytes: str = '1000M'

	# TODO: only set things that crunchyroll actually uses
	slang: str = 'en,enUS,eng,en'
	alang: str = 'jp,jpn,en'

	ytdl_raw_options: str = "config-locations=" + yt_dlp_config_dir

	# Used for debugging
	vf_add: str = "rotate=PI/2"

	include: str = mpv_config_dir + '/user.conf'

	def __init__(self):
		if checkBaseDir() == False or self.checkConfigDir() == False:
			self.save()
			self.createUserConf()
			return

		if self.checkUserConfFile() == False:
			self.createUserConf()

		if self.checkConfigFile() == False:
			self.save()
			return

		# Load config
		config = configparser.ConfigParser()
		config.read(mpv_config_dir + '/mpv.conf')

		if 'default' in config:
			config = config['default']

			if 'cache' in config:
				self.cache = config['cache']

			if 'demuxer-max-bytes' in config:
				self.demuxer_max_bytes = config['demuxer-max-bytes']

			if 'demuxer-max-back-bytes' in config:
				self.demuxer_max_back_bytes = config['demuxer-max-back-bytes']

			if 'slang' in config:
				self.slang = config['slang']

			if 'alang' in config:
				self.alang = config['alang']

			if 'ytdl-raw-options' in config:
				self.ytdl_raw_options = config['ytdl-raw-options']

			if 'include' in config:
				self.include = config['include']

	def checkConfigDir(self):
		return os.path.exists(mpv_config_dir)

	def checkConfigFile(self):
		return os.path.exists(mpv_config_dir + '/mpv.conf')

	def checkUserConfFile(self):
		return os.path.exists(mpv_config_dir + '/user.conf')

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(config_dir)

		if self.checkConfigDir() == False:
			os.mkdir(mpv_config_dir)

		config = configparser.ConfigParser()
		config['default'] = {
			'cache': self.cache,
			'demuxer-max-bytes': self.demuxer_max_bytes,
			'demuxer-max-back-bytes': self.demuxer_max_back_bytes,
			'slang': self.slang,
			'alang': self.alang,
			'ytdl-raw-options': self.ytdl_raw_options,
			'vf-add': self.vf_add,
			'include': self.include
		}

		# Create the config file
		conf_file = open(mpv_config_dir + '/mpv.conf', 'w')
		config.write(conf_file, space_around_delimiters=False)
		conf_file.close()

		# Set the permissions
		os.chmod(mpv_config_dir + '/mpv.conf', 0o600)

	def createUserConf(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(config_dir)

		if self.checkConfigDir() == False:
			os.mkdir(mpv_config_dir)

		# Create the config file
		conf_file = open(mpv_config_dir + '/user.conf', 'w')
		conf_file.write('# This file is automatically created by Openroll if it does not exist\n')
		conf_file.write('# Any setting in this file should override the settings in mpv.conf\n')
		conf_file.close()

		# Set the permissions
		os.chmod(mpv_config_dir + '/user.conf', 0o600)
