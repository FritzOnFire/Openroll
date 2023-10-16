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

def setScaleFactor(height: int):
	if config.disable_scale_factor:
		print("Scale factor disabled by config")
		return

	# *Sad hardcoded value noises*
	global scaleFactor

	if height == 2160:
		scaleFactor = 2.0
	scaleFactor = 1.0

def scale(value: float):
	"""
		Apply the scale factor to a value
	"""
	return int(value * scaleFactor)
