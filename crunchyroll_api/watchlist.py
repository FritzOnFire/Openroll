class EpisodeVersion:
	audio_locale: str = None
	guid: str = None
	is_premium_only: bool = None
	media_guid: str = None
	original: bool = None
	season_guid: str = None
	variant: str = None

	def __init__(self, json) -> None:
		if 'audio_locale' in json:
			self.audio_locale = json['audio_locale']

		if 'guid' in json:
			self.guid = json['guid']

		if 'is_premium_only' in json:
			self.is_premium_only = json['is_premium_only']

		if 'media_guid' in json:
			self.media_guid = json['media_guid']

		if 'original' in json:
			self.original = json['original']

		if 'season_guid' in json:
			self.season_guid = json['season_guid']

		if 'variant' in json:
			self.variant = json['variant']

class EpisodeMetadata:
	audio_locale: str = None
	availability_ends: str = None
	availability_notes: str = None
	availability_starts: str = None
	available_date: str = None
	available_offline: bool = None
	closed_captions_available: bool = None
	duration_ms: int = None
	eligible_region: str = None
	episode: str = None
	episode_air_date: str = None
	episode_number: int = None
	extended_maturity_rating: dict = None
	free_available_date: str = None
	identifier: str = None
	is_clip: bool = None
	is_dubbed: bool = None
	is_mature: bool = None
	is_premium_only: bool = None
	is_subbed: bool = None
	mature_blocked: bool = None
	maturity_ratings: list[str] = None
	premium_available_date: str = None
	premium_date: str = None
	season_id: str = None
	season_number: int = None
	season_slug_title: str = None
	season_title: str = None
	sequence_number: int = None
	series_id: str = None
	series_slug_title: str = None
	series_title: str = None
	subtitle_locales: list[str] = None
	tenant_categories: list[str] = None
	upload_date: str = None
	versions: list[EpisodeVersion] = []

	def __init__(self, json) -> None:
		if 'audio_locale' in json:
			self.audio_locale = json['audio_locale']

		if 'availability_ends' in json:
			self.availability_ends = json['availability_ends']

		if 'availability_notes' in json:
			self.availability_notes = json['availability_notes']

		if 'availability_starts' in json:
			self.availability_starts = json['availability_starts']

		if 'available_date' in json:
			self.available_date = json['available_date']

		if 'available_offline' in json:
			self.available_offline = json['available_offline']

		if 'closed_captions_available' in json:
			self.closed_captions_available = json['closed_captions_available']

		if 'duration_ms' in json:
			self.duration_ms = json['duration_ms']

		if 'eligible_region' in json:
			self.eligible_region = json['eligible_region']

		if 'episode' in json:
			self.episode = json['episode']

		if 'episode_air_date' in json:
			self.episode_air_date = json['episode_air_date']

		if 'episode_number' in json:
			self.episode_number = json['episode_number']

		if 'extended_maturity_rating' in json:
			self.extended_maturity_rating = json['extended_maturity_rating']

		if 'free_available_date' in json:
			self.free_available_date = json['free_available_date']

		if 'identifier' in json:
			self.identifier = json['identifier']

		if 'is_clip' in json:
			self.is_clip = json['is_clip']

		if 'is_dubbed' in json:
			self.is_dubbed = json['is_dubbed']

		if 'is_mature' in json:
			self.is_mature = json['is_mature']

		if 'is_premium_only' in json:
			self.is_premium_only = json['is_premium_only']

		if 'is_subbed' in json:
			self.is_subbed = json['is_subbed']

		if 'mature_blocked' in json:
			self.mature_blocked = json['mature_blocked']

		if 'maturity_ratings' in json:
			self.maturity_ratings = json['maturity_ratings']

		if 'premium_available_date' in json:
			self.premium_available_date = json['premium_available_date']

		if 'premium_date' in json:
			self.premium_date = json['premium_date']

		if 'season_id' in json:
			self.season_id = json['season_id']

		if 'season_number' in json:
			self.season_number = json['season_number']

		if 'season_slug_title' in json:
			self.season_slug_title = json['season_slug_title']

		if 'season_title' in json:
			self.season_title = json['season_title']

		if 'sequence_number' in json:
			self.sequence_number = json['sequence_number']

		if 'series_id' in json:
			self.series_id = json['series_id']

		if 'series_slug_title' in json:
			self.series_slug_title = json['series_slug_title']

		if 'series_title' in json:
			self.series_title = json['series_title']

		if 'subtitle_locales' in json:
			self.subtitle_locales = json['subtitle_locales']

		if 'tenant_categories' in json:
			self.tenant_categories = json['tenant_categories']

		if 'upload_date' in json:
			self.upload_date = json['upload_date']

		if 'versions' in json:
			for version in json['versions']:
				self.versions.append(EpisodeVersion(version))

class Thumbnail:
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

class Images:
	thumbnail: list[list[Thumbnail]] = []

	def __init__(self, json) -> None:
		if 'thumbnail' in json:
			for thumbnail in json['thumbnail']:
				sub = []
				for sub_thumbnail in thumbnail:
					sub.append(Thumbnail(sub_thumbnail))
				self.thumbnail.append(sub)

class Panel:
	promo_description: str = None
	slug: str = None
	streams_link: str = None
	type: str = None
	external_id: str = None
	id: str = None
	channel_id: str = None
	promo_title: str = None
	title: str = None
	episode_metadata: EpisodeMetadata = None
	images: Images = None
	slug_title: str = None
	linked_resource_key: str = None
	description: str = None

	def __init__(self, json) -> None:
		if 'promo_description' in json:
			self.promo_description = json['promo_description']

		if 'slug' in json:
			self.slug = json['slug']

		if 'streams_link' in json:
			self.streams_link = json['streams_link']

		if 'type' in json:
			self.type = json['type']

		if 'external_id' in json:
			self.external_id = json['external_id']

		if 'id' in json:
			self.id = json['id']

		if 'channel_id' in json:
			self.channel_id = json['channel_id']

		if 'promo_title' in json:
			self.promo_title = json['promo_title']

		if 'title' in json:
			self.title = json['title']

		if 'episode_metadata' in json:
			self.episode_metadata = EpisodeMetadata(json['episode_metadata'])

		if 'images' in json:
			self.images = Images(json['images'])

		if 'slug_title' in json:
			self.slug_title = json['slug_title']

		if 'linked_resource_key' in json:
			self.linked_resource_key = json['linked_resource_key']

		if 'description' in json:
			self.description = json['description']

class Data:
	panel: Panel = None
	new: bool = None
	is_favorite: bool = None
	fully_watched: bool = None
	never_watched: bool = None
	playhead: int = None

	def __init__(self, json) -> None:
		if 'panel' in json:
			self.panel = Panel(json['panel'])

		if 'new' in json:
			self.new = json['new']

		if 'is_favorite' in json:
			self.is_favorite = json['is_favorite']

		if 'fully_watched' in json:
			self.fully_watched = json['fully_watched']

		if 'never_watched' in json:
			self.never_watched = json['never_watched']

		if 'playhead' in json:
			self.playhead = json['playhead']

class Meta:
	total_before_filter: int = None

	def __init__(self, json) -> None:
		if 'total_before_filter' in json:
			self.total_before_filter = json['total_before_filter']

class WatchlistResponse:
	total: int = None
	data: list[Data] = []
	meta: Meta = None

	def __init__(self, json) -> None:
		if 'total' in json:
			self.total = json['total']

		if 'data' in json:
			for data in json['data']:
				self.data.append(Data(data))

		if 'meta' in json:
			self.meta = Meta(json['meta'])
