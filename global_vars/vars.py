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

	sf = 1.0

	# *Sad hardcoded value noises*
	if height == 2160:
		sf = 2.0
	elif height == 1440:
		sf = 1.5

	global scaleFactor
	scaleFactor = sf

def scale(value: float):
	"""
		Apply the scale factor to a value
	"""
	return int(value * scaleFactor)
