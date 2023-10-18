import os

from global_vars.constants import config_dir, yt_dlp_config_dir

from utils.config import checkBaseDir

class YTDLPConfig:
	concurrent_fragments: int = 2
	cookies: str = yt_dlp_config_dir + '/cookies.txt'
	user_agent: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

	# Used during development
	cookies_from_browser: str = None

	# TODO: set format options

	def __init__(self):
		# Used during development
		self.cookies_from_browser = "chrome"

		if checkBaseDir() == False or self.checkConfigDir() == False or self.checkConfigFile() == False:
			self.save()
			return

		conf_file = open(yt_dlp_config_dir + '/config', 'r')
		conf_file_lines = conf_file.readlines()
		conf_file.close()

		for line in conf_file_lines:
			args = line.split(' ')
			for arg in args:
				if arg.startswith('--concurrent-fragments='):
					self.concurrent_fragments = int(arg.split('=')[1])
					continue
				if arg.startswith('--cookies='):
					self.cookies = arg.split('=')[1]
					continue

	def checkConfigDir(self):
		return os.path.exists(yt_dlp_config_dir)

	def checkConfigFile(self):
		return os.path.exists(yt_dlp_config_dir + '/config')

	def save(self):
		# Create the config directory
		if checkBaseDir() == False:
			os.mkdir(config_dir)

		if self.checkConfigDir() == False:
			os.mkdir(yt_dlp_config_dir)

		# Create the config file
		conf_file = open(yt_dlp_config_dir + '/config', 'w')

		if self.concurrent_fragments:
			conf_file.write('--concurrent-fragments ' + str(self.concurrent_fragments))
			conf_file.write(' ')

		if self.cookies_from_browser:
			conf_file.write('--cookies-from-browser ' + self.cookies_from_browser)
			conf_file.write(' ')
		else:
			conf_file.write('--cookies ' + self.cookies)
			conf_file.close(' ')

		if self.user_agent:
			conf_file.write('--user-agent ' + self.user_agent)
			conf_file.write(' ')

		# Set the permissions
		os.chmod(yt_dlp_config_dir + '/config', 0o600)
