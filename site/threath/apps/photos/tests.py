import os
import simplejson
from testing.testcases import MongoTestCase
from django.contrib.auth.models import User
from django.test.client import Client
from group.models import Group
from photos.models import Photo, get_picture_from_url
from django.conf import settings

media_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media_for_testing')

#sample_gif = os.path.join(media_dir, 'potatoes.gif')
sample_jpeg = os.path.join(media_dir, 'rock-into-mordor.jpg')

class TestPhoto(MongoTestCase):
    
    def setUp(self):
        self.c = Client()
        self.u = User.objects.create_user(username="testuser", email="user@test.com", password="pass")
        self.c.login(username="testuser", password="pass")
        
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")

        self.m_group = Group.objects.ensure_mutual_group(self.user1, self.user2)
        
        self.jpeg = open(sample_jpeg, 'r')
        self.jpeg2 = open(sample_jpeg, 'r')
        
        # response = self.c.post('/api/photos/', {
        #     'title': "hello photo",
        #     'file': self.jpeg,
        #     'description':"test 1234",
        # })
        # response_json = self.get_dict(response)
        # self.photo1 = Photo.objects.get(id=response_json['response']['id'])
        
        # response = self.c.post('/api/photos/', {
        #     'title': "hello photo2",
        #     'file': self.jpeg2,
        #     'description':"test 1234",
        # })
        # response_json = self.get_dict(response)
        # self.photo2 = Photo.objects.get(id=response_json['response']['id'])
    
    def tearDown(self):
        self.jpeg.close()
        self.jpeg2.close()
        for photo in Photo.objects.all():
            photo.delete()
        
    # def test_basic(self):
        
    #     # attach object
    #     self.assertEqual(self.photo1.object_id, None)
    #     self.photo1.attach(self.user1)
    #     self.assertEqual(self.photo1.object_id, self.user1.id)
        
    #     self.assertEqual(self.photo1.get_photo_url(), '%s%s' % (settings.MEDIA_URL, self.photo1.ImageJpeg.name))
    #     self.assertEqual(self.photo1.get_absolute_url(), '%s%s' % (settings.MEDIA_URL, self.photo1.ImageJpeg.name))
        
    #     self.assertEqual(self.photo1.to_json(), {
    #         'thumb_sepia': '%s%s' % (settings.MEDIA_URL, self.photo1.sepia50x50.name),
    #         'id': self.photo1.id,
    #         'thumb': '%s%s' % (settings.MEDIA_URL, self.photo1.image50x50.name)
    #     })
        
    #     detail_json = self.photo1.to_json(detail=True)
    #     self.assertEqual(detail_json['large'], '%s%s' % (settings.MEDIA_URL, self.photo1.image450x450.name))
    #     self.assertEqual(detail_json['user_id'], self.photo1.user.id)
        
    #     self.assertEqual(self.photo1.imagefit128x128.url, '%s%s' % (settings.MEDIA_URL, self.photo1.imagefit128x128.name))
    #     self.assertEqual(self.photo1.image388xany.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image388xany.name))
    #     self.assertEqual(self.photo1.image24x24.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image24x24.name))
    #     self.assertEqual(self.photo1.image25x25.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image25x25.name))
    #     self.assertEqual(self.photo1.image26x26.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image26x26.name))
    #     self.assertEqual(self.photo1.image32x32.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image32x32.name))
    #     self.assertEqual(self.photo1.sepia32x32.url, '%s%s' % (settings.MEDIA_URL, self.photo1.sepia32x32.name))
    #     self.assertEqual(self.photo1.image40x40.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image40x40.name))
    #     self.assertEqual(self.photo1.image50x50.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image50x50.name))
    #     self.assertEqual(self.photo1.sepia50x50.url, '%s%s' % (settings.MEDIA_URL, self.photo1.sepia50x50.name))
    #     self.assertEqual(self.photo1.image60x37.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image60x37.name))
    #     self.assertEqual(self.photo1.image77x77.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image77x77.name))
    #     self.assertEqual(self.photo1.image98x98.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image98x98.name))
    #     self.assertEqual(self.photo1.image105x105.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image105x105.name))
    #     self.assertEqual(self.photo1.image134x134.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image134x134.name))
    #     self.assertEqual(self.photo1.image146x146.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image146x146.name))
    #     self.assertEqual(self.photo1.image147x113.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image147x113.name))
    #     self.assertEqual(self.photo1.image150x150.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image150x150.name))
    #     self.assertEqual(self.photo1.image153x153.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image153x153.name))
    #     self.assertEqual(self.photo1.image160x160.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image160x160.name))
    #     self.assertEqual(self.photo1.image186x119.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image186x119.name))
    #     self.assertEqual(self.photo1.image307x307.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image307x307.name))
    #     self.assertEqual(self.photo1.image405x405.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image405x405.name))
    #     self.assertEqual(self.photo1.image450x450.url, '%s%s' % (settings.MEDIA_URL, self.photo1.image450x450.name))
        
    #     # photo view
    #     response = self.c.get('%s%s/50/50/' % ('/photos/', self.photo1.id))
    #     self.assertEqual(response.content, self.photo1.image50x50.url)
        
    #     response = self.c.get('%s%s/50/50/' % ('/photos/user/', self.user1.id))
        
    #     self.assertTrue(self.user1.get_profile().get_display_photo().image50x50.url in str(response))
        
    #     # test delete user
    #     self.assertEqual(Photo.objects.filter(user=self.u).count(), 2)
    #     self.u.delete()
    #     self.assertEqual(Photo.objects.filter(user=self.u).count(), 0)
        
        # test get_picture_from_url
        # TODO
        
        
    def get_dict(self, response):
        """ Ensures response returned with HTTP 200 and deserializes response
        json body. """
        self.assertTrue(response.status_code, 200)
        response_json = simplejson.loads(response.content)
        return response_json