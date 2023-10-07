from crunchyroll_api.api import CrunchyrollAPI
from .config import Config

config: Config = Config()
crunchyroll: CrunchyrollAPI = None
premium_user: bool = False

def init():
	global crunchyroll
	config.load()

	crunchyroll = CrunchyrollAPI(config.device_id)
