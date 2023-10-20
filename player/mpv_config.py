import os
import configparser

from global_vars.constants import config_dir, mpv_config_dir, yt_dlp_config_dir

from utils.config import checkBaseDir

class MPVConfig:
	osc: str = 'yes'
	osd_bar: str = 'no'
	osd_font: str = 'Lato'
	osd_blur: str = '19.0'
	osd_color: str = '#f47521' # Not sure about this colour yet
	input_default_bindings: str = 'yes'
	input_vo_keyboard: str = 'yes'
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

			if 'osc' in config:
				self.osc = config['osc']

			if 'osd-bar' in config:
				self.osd_bar = config['osd-bar']

			if 'osd-font' in config:
				self.osd_font = config['osd-font']

			if 'osd-blur' in config:
				self.osd_blur = config['osd-blur']

			if 'osd-color' in config:
				self.osd_color = config['osd-color']

			if 'input-default-bindings' in config:
				self.input_default_bindings = config['input-default-bindings']

			if 'input-vo-keyboard' in config:
				self.input_vo_keyboard = config['input-vo-keyboard']

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
			'osc': self.osc,
			'osd-bar': self.osd_bar,
			'osd-font': self.osd_font,
			'osd-blur': self.osd_blur,
			'osd-color': self.osd_color,
			'input-default-bindings': self.input_default_bindings,
			'input-vo-keyboard': self.input_vo_keyboard,
			'cache': self.cache,
			'demuxer-max-bytes': self.demuxer_max_bytes,
			'demuxer-max-back-bytes': self.demuxer_max_back_bytes,
			'slang': self.slang,
			'alang': self.alang,
			'ytdl-raw-options': self.ytdl_raw_options,
			# 'vf-add': self.vf_add,
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

class MPVInput:
	m_btn_left: str = "ignore"
	m_btn_left_dbl: str = "cycle fullscreen"
	m_btn_right: str = "cycle pause"

	def __init__(self):
		if checkBaseDir() == False or self.checkConfigDir() == False or self.checkConfigFile() == False:
			self.save()
			return

		# Load config
		config = configparser.ConfigParser(delimiters=(' '))
		config.read(mpv_config_dir + '/input.conf')

		if 'default' in config:
			config = config['default']

			if 'MBTN_LEFT' in config:
				self.m_btn_left = config['MBTN_LEFT']

			if 'MBTN_LEFT_DBL' in config:
				self.m_btn_left_dbl = config['MBTN_LEFT_DBL']

			if 'MBTN_RIGHT' in config:
				self.m_btn_right = config['MBTN_RIGHT']

	def checkConfigDir(self):
		return os.path.exists(mpv_config_dir)

	def checkConfigFile(self):
		return os.path.exists(mpv_config_dir + '/input.conf')

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(config_dir)

		if self.checkConfigDir() == False:
			os.mkdir(mpv_config_dir)

		config = configparser.ConfigParser(delimiters=(' '))
		config['default'] = {
			'MBTN_LEFT': self.m_btn_left,
			'MBTN_LEFT_DBL': self.m_btn_left_dbl,
			'MBTN_RIGHT': self.m_btn_right
		}

		# Create the config file
		conf_file = open(mpv_config_dir + '/input.conf', 'w')
		config.write(conf_file, space_around_delimiters=False)
		conf_file.close()

		# Set the permissions
		os.chmod(mpv_config_dir + '/input.conf', 0o600)
