from django.conf import settings

from testing.testcases import MongoTestCase
from place.models import FoursquarePlace

class FoursquarePlaceModelTest(MongoTestCase):
	def setUp(self):
		pass

	def test_fs_search(self):
		kwargs = {
			'll': '40.755527,-73.981675',
			'q': 'Bistro',
		}
		venues = FoursquarePlace.objects.spatial_search(**kwargs)

	def tearDown(self):
		pass