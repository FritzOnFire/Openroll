import os
import hashlib
import requests

THUMBNAIL_CACHE_DIR = '/tmp/openroll/cache/thumbnails'

def getThumbnail(url: str) -> bytes:
	thumbnail, ok = checkChache(url)
	if ok:
		return thumbnail

	session = requests.Session()
	responce = session.get(url)
	if responce.ok == False:
		raise Exception('while downloading thumbnail: ' + responce.text)

	thumbnail = responce.content
	saveToCache(url, thumbnail)
	return thumbnail

def checkChache(url: str) -> (bytes, bool):
	if os.path.exists(THUMBNAIL_CACHE_DIR) != True:
		os.makedirs(THUMBNAIL_CACHE_DIR)
		return None, False

	hash = hashlib.md5(url.encode('utf-8')).hexdigest()
	path = THUMBNAIL_CACHE_DIR + '/' + hash
	if os.path.exists(path) != True:
		return None, False

	with open(path, 'rb') as f:
		return f.read(), True

def saveToCache(url: str, thumbnail: bytes):
	hash = hashlib.md5(url.encode('utf-8')).hexdigest()
	path = THUMBNAIL_CACHE_DIR + '/' + hash
	with open(path, 'wb') as f:
		f.write(thumbnail)
