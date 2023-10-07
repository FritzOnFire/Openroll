import os

def checkBaseDir():
	return os.path.exists(os.path.expanduser('~/.config/openroll'))
