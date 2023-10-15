class Image:
	height: int = None
	source: str = None
	type: str = None
	width: int = None

	def __init__(self, json) -> None:
		if 'height' in json:
			self.height = json['height']

		if 'source' in json:
			self.source = json['source']

		if 'type' in json:
			self.type = json['type']

		if 'width' in json:
			self.width = json['width']
