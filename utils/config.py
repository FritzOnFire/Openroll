import os

import global_vars.constants as c

def checkBaseDir():
	return os.path.exists(c.config_dir)
