from collections import namedtuple

"""
Model to spec mapping is an 1 to n relation.
"""
CARD_TYPE_UNDEFINED = 0
CARD_TYPE_LINK = 1
CARD_TYPE_PHOTO = 2
CARD_TYPE_VIDEO = 3
CARD_TYPE_MOVIE = 4
CARD_TYPE_RESTAURANT = 5
CARD_TYPE_CONTACT = 6

CARD_MAP = {
    "UNDEFINED": (CARD_TYPE_UNDEFINED, 'Undefined', []),
    "LINK": (CARD_TYPE_LINK, 'Link', ['id', 'title', 'picture', 'url', 'domain', 'description', 'picture_url', 'youtube_id', ]),
    "PHOTO": (CARD_TYPE_PHOTO, 'Photo', ['id', 'title', 'picture', 'filesize', 'photo_source']),
    "VIDEO": (CARD_TYPE_VIDEO, 'Video', ['id', 'title', 'url', 'picture', 'filesize', 'runtime']),
    "MOVIE": (CARD_TYPE_MOVIE, 'Movie showtime', ['id', 'title', 'picture', 'year', 'runtime', 'critics_score', 'mpaa_rating', 'showtime', 'theater_name', 'expiry', 'expiry_str']),
    "RESTAURANT": (CARD_TYPE_RESTAURANT, 'Restaurant', ['id', 'title', 'picture', 'category_list', 'address', 'rating', 'rating_img_url', 'display_phone']),
    "CONTACT": (CARD_TYPE_CONTACT, 'Contact', ['id', 'title', 'picture', 'phone_display', 'email_display']),
}
sorted_keys = sorted(CARD_MAP, key=lambda x: CARD_MAP[x][0])

CARD_TYPE = namedtuple('CARD_TYPE', sorted_keys)(**dict([(k, v[0]) for k, v in CARD_MAP.items()]))
CARD_TYPE_CHOICE = [(v[0], k) for k, v in CARD_MAP.items()]
CARD_TYPE_STRING = namedtuple('CARD_TYPE_STRING', sorted_keys)(**dict([(k, k.lower()) for k, v in CARD_MAP.items()]))
CARD_NAME = namedtuple('CARD_NAME', sorted_keys)(**dict([(k, v[1]) for k, v in CARD_MAP.items()]))
CARD_SPEC = namedtuple('CARD_SPEC', sorted_keys)(**dict([(k, v[2]) for k, v in CARD_MAP.items()]))

