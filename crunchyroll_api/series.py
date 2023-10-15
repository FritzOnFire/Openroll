from crunchyroll_api.common_responce_classes import Image

class SeriesMetadata:
	audio_locales: list[str] = None
	availability_notes: str = None
	episode_count: int = None
	extended_description: str = None
	extended_maturity_rating: str = None
	is_dubbed: bool = None
	is_mature: bool = None
	is_simulcast: bool = None
	is_subbed: bool = None
	mature_blocked: bool = None
	maturity_ratings: list[str] = None
	season_count: int = None
	series_launch_year: int = None
	subtitle_locales: list[str] = None
	tenant_categories: list[str] = None

	def __init__(self, json):
		if 'audio_locales' in json:
			self.audio_locales = json['audio_locales']

		if 'availability_notes' in json:
			self.availability_notes = json['availability_notes']

		if 'episode_count' in json:
			self.episode_count = json['episode_count']

		if 'extended_description' in json:
			self.extended_description = json['extended_description']

		if 'extended_maturity_rating' in json:
			self.extended_maturity_rating = json['extended_maturity_rating']

		if 'is_dubbed' in json:
			self.is_dubbed = json['is_dubbed']

		if 'is_mature' in json:
			self.is_mature = json['is_mature']

		if 'is_simulcast' in json:
			self.is_simulcast = json['is_simulcast']

		if 'is_subbed' in json:
			self.is_subbed = json['is_subbed']

		if 'mature_blocked' in json:
			self.mature_blocked = json['mature_blocked']

		if 'maturity_ratings' in json:
			self.maturity_ratings = json['maturity_ratings']

		if 'season_count' in json:
			self.season_count = json['season_count']

		if 'series_launch_year' in json:
			self.series_launch_year = json['series_launch_year']

		if 'subtitle_locales' in json:
			self.subtitle_locales = json['subtitle_locales']

		if 'tenant_categories' in json:
			self.tenant_categories = json['tenant_categories']

class Star:
	displayed: str = None
	percentage: int = None
	unit: str = None

	def __init__(self, json):
		if 'displayed' in json:
			self.displayed = json['displayed']

		if 'percentage' in json:
			self.percentage = json['percentage']

		if 'unit' in json:
			self.unit = json['unit']

class Rating:
	one_star: Star = None
	two_star: Star = None
	three_star: Star = None
	four_star: Star = None
	five_star: Star = None
	average: str = None
	total: int = None

	def __init__(self, json):
		if 'one_star' in json:
			self.one_star = Star(json['1s'])

		if 'two_star' in json:
			self.two_star = Star(json['2s'])

		if 'three_star' in json:
			self.three_star = Star(json['3s'])

		if 'four_star' in json:
			self.four_star = Star(json['4s'])

		if 'five_star' in json:
			self.five_star = Star(json['5s'])

		if 'average' in json:
			self.average = json['average']

		if 'total' in json:
			self.total = json['total']

class Images:
	poster_tall: list[list[Image]] = None
	poster_wide: list[list[Image]] = None

	def __init__(self, json):
		self.poster_tall = []
		self.poster_wide = []

		if 'poster_tall' in json:
			for image in json['poster_tall']:
				sub: list[Image] = []
				for sub_image in image:
					sub.append(Image(sub_image))
				self.poster_tall.append(sub)

		if 'poster_wide' in json:
			for image in json['poster_wide']:
				sub: list[Image] = []
				for sub_image in image:
					sub.append(Image(sub_image))
				self.poster_wide.append(sub)

class Data:
	description: str = None
	id: str = None
	promo_title: str = None
	title: str = None
	series_metadata: SeriesMetadata = None
	channel_id: str = None
	external_id: str = None
	promo_description: str = None
	slug_title: str = None
	linked_resource_key: str = None
	rating: Rating = None
	images: Images = None
	slug: str = None
	type: str = None

	def __init__(self, json):
		if 'description' in json:
			self.description = json['description']

		if 'id' in json:
			self.id = json['id']

		if 'promo_title' in json:
			self.promo_title = json['promo_title']

		if 'title' in json:
			self.title = json['title']

		if 'series_metadata' in json:
			self.series_metadata = SeriesMetadata(json['series_metadata'])

		if 'channel_id' in json:
			self.channel_id = json['channel_id']

		if 'external_id' in json:
			self.external_id = json['external_id']

		if 'promo_description' in json:
			self.promo_description = json['promo_description']

		if 'slug_title' in json:
			self.slug_title = json['slug_title']

		if 'linked_resource_key' in json:
			self.linked_resource_key = json['linked_resource_key']

		if 'rating' in json:
			self.rating = Rating(json['rating'])

		if 'images' in json:
			self.images = Images(json['images'])

		if 'slug' in json:
			self.slug = json['slug']

		if 'type' in json:
			self.type = json['type']

	def thumbnailURL(self) -> str:
		if self.images == None:
			return ""

		if self.images.poster_wide == None:
			return ""

		if len(self.images.poster_wide) == 0:
			return ""

		if len(self.images.poster_wide[0]) == 0:
			return ""

		return self.images.poster_wide[0][0].source


class SeriesResponse:
	data: list[Data] = None
	meta: dict = None
	total: int = None

	dataDict: dict[str, Data] = None

	def __init__(self, json):
		self.data = []
		self.meta = {}

		if 'data' in json:
			for data in json['data']:
				self.data.append(Data(data))

		if 'meta' in json:
			self.meta = json['meta']

		if 'total' in json:
			self.total = json['total']

		self.dataDict = {}
		for data in self.data:
			self.dataDict[data.id] = data
