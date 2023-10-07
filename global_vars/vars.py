from crunchyroll_api.config import CRConfig
from crunchyroll_api.api import CrunchyrollAPI
from .config import Config

config: Config = Config()
crunchyroll: CrunchyrollAPI = None
cr_config: CRConfig = CRConfig()
premium_user: bool = False

def init():
	global crunchyroll
	crunchyroll = CrunchyrollAPI(config.device_id, cr_config)
