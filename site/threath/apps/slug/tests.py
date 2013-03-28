from django.contrib.auth.models import User
from testing.testcases import MongoTestCase
from slug.models import Slug
import re

class Test_Meta(MongoTestCase):

    def setUp(self):
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username="user2")
        self.exist_slug = Slug(content_object=self.user1, slug="test_slug")
        self.exist_slug.save()

    def test_validate(self):
        """
        test validate
        """

        str1 = 'g-e-nie'
        str2 = '12345'
        str3 = '123456'
        str4 = '123'
        str5 = '123456789012345'
        str6 = '1234567890123456'
        str7 = 'admin'
        str8 = 'test_slug'

        self.assertTrue(not Slug.objects.validate(str1))
        self.assertTrue(Slug.objects.validate(str2))
        self.assertTrue(Slug.objects.validate(str3))
        self.assertTrue(not Slug.objects.validate(str4))
        self.assertTrue(Slug.objects.validate(str5))
        self.assertTrue(not Slug.objects.validate(str6))
        self.assertTrue(not Slug.objects.validate(str7))
        self.assertTrue(not Slug.objects.validate(str8))

    def test_sluggify(self):
        """
        test sluggify function
        """
        str1 = 'g-e-nie'
        str2 = 'g e n i e'
        str3 = 'G E-ni e'
        str4 = 'gen'
        str5 = '1234567890123456'
        str6 = '123456789012345'

        self.assertEqual(Slug.objects.sluggify(str1), 'g_e_nie')
        self.assertEqual(Slug.objects.sluggify(str2), 'g_e_n_i_e')
        self.assertEqual(Slug.objects.sluggify(str3), 'g_e_ni_e')
        self.assertRegexpMatches(Slug.objects.sluggify(str4), 'gen[a-z0-9]{2}')
        #self.assertEqual(Slug.objects.sluggify(str4), 'geni_____')
        self.assertEqual(Slug.objects.sluggify(str5), '123456789012345')

        self.newslug = Slug(content_object=self.user1, slug="123456789012345")
        self.newslug.save()

        self.assertEqual(Slug.objects.sluggify(str6), '123456789012341')

    def test_change_slug_name(self):
        """
        test change slug name function
        """
        success = self.exist_slug.change_slug_name('admin')
        self.assertTrue(not success)
        self.assertEqual(self.exist_slug.slug, 'test_slug')

        success = self.exist_slug.change_slug_name('genie1')
        self.assertTrue(success)
        self.assertEqual(self.exist_slug.slug, 'genie1')

        success = self.exist_slug.change_slug_name('genie2')
        self.assertTrue(success)
        self.assertEqual(self.exist_slug.slug, 'genie2')

        success = self.exist_slug.change_slug_name('genie3')
        self.assertTrue(success)
        self.assertEqual(self.exist_slug.slug, 'genie3')

        success = self.exist_slug.change_slug_name('genie4')
        self.assertTrue(not success)
        self.assertEqual(self.exist_slug.slug, 'genie3')

