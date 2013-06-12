from django.contrib.auth.models import User
from testing.testcases import MongoTestCase
from youtube.models import YoutubeVideo

class TestYoutubeVideoModel(MongoTestCase):
    def setUp(self):
        pass

    def test_model(self):
        options = {
            'q':'snsd'
        }
        YoutubeVideo.objects.youtube_search(options)