from crunchyroll_api.config import CRConfig
from crunchyroll_api.api import CrunchyrollAPI
from .config import Config

config: Config = Config()
crunchyroll: CrunchyrollAPI = None
cr_config: CRConfig = CRConfig()
premium_user: bool = False
scaleFactor: float = 1.0

def init():
	global crunchyroll
	crunchyroll = CrunchyrollAPI(config.device_id, cr_config)

def setScaleFactor(dpi: float):
	if config.disable_scale_factor:
		print("Scale factor disabled by config")
		return

	# *Sad hardcoded DPI values noises*
	global scaleFactor

	# Should cater for a 1080p screen
	if dpi < 50:
		scaleFactor = 1.0

	# Should cater for a 1440p screen
	elif dpi < 108:
		scaleFactor = 1.5

	# Should cater for a 4k screen
	else:
		scaleFactor = 2.0

def scale(value: float):
	"""
		Apply the scale factor to a value
	"""
	return int(value * scaleFactor)
