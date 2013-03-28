#"""
#
#"""
#__author__ = "Greg Coleman <traderwerks@gmail.com>"
#
#import pdb
#import datetime
#import unittest
#from django.test import TestCase
#from django.shortcuts import get_object_or_404
#from django.contrib.contenttypes.models import ContentType
#from iptolocation.models import IPToCountry, IPToLocation, Country, Location, IPRange, Blocks
#
#class IPToLocationTest(unittest.TestCase):
#
#    @classmethod
#    def setUp(self):
#        """
#        Not much
#        """
#        self.ip2country = IPToCountry.objects.create()
#        self.ip2location  = IPToLocation.objects.create()
#        
#        # some ip range data
#        au_country = Country.objects.create(code='AU', name= 'kangaroo-land')
#        cn_country = Country.objects.create(code='CN', name= 'Commie-land')
#        jp_country = Country.objects.create(code='JP', name= 'Sony-land')
#        th_country = Country.objects.create(code='TH', name= 'You-Know-What-land')
#        tw_country = Country.objects.create(code='TW', name= 'Best Country In The WORLD-land')
#        ip = IPRange.objects.create(country = au_country, start = 16777216, end = 16777471 )
#        ip.save()
#        ip = IPRange.objects.create(country = cn_country, start = 16777472, end = 16778239 )
#        ip.save()
#        ip = IPRange.objects.create(country = au_country, start = 16778240, end = 16779263 )
#        ip.save()
#        ip = IPRange.objects.create(country = cn_country, start = 16779264, end = 16781311 )
#        ip.save()
#        ip = IPRange.objects.create(country = jp_country, start = 16781312, end = 16785407 )
#        ip.save()
#        ip = IPRange.objects.create(country = cn_country, start = 16785408, end = 16793599 )
#        ip.save()
#        ip = IPRange.objects.create(country = jp_country, start = 16793600, end = 16809983 )
#        ip.save()
#        ip = IPRange.objects.create(country = th_country, start = 16809984, end = 16842751 )
#        ip.save()
#        ip = IPRange.objects.create(country = tw_country, start = 19005440, end = 19136511 )
#        ip.save()
#
#        l = Location.objects.create(loc_id=100,country="TW",region="TW",city="TW",postal_code="TW",latitude="22.22",longitude="33.33",metro_code="TW",area_code="TW")
#        l.save()
#        
#        bloc = Blocks.objects.create(loc = l, start = 3706025080, end   = 3706025188)
#        bloc.save()
#
#
#    def test_ip_to_country(self):
#        """
#        test with TH as default   1.0.128.0
#        """
#        located_country = self.ip2country.find_country_from_ipaddress("1.0.128.0")
#        self.assertEqual("TH", located_country , msg="Looking up Thaland ip address for nation") 
#
#    def test_ip_to_country_japan(self):
#        """
#        { "_id" : ObjectId("4dc7821260eed214e700cf94"), "cc" : "JP", "start" : 16781312, "end" : 16785407 }
#        """
#        located_japan = self.ip2country.find_country_from_long(16781318)
#        self.assertEqual("JP", located_japan , msg="Looking up ip address for Japan") 
#        
#    def test_ip_to_location(self):
#        """
#        test with ip address in taipei
#        """
#        
#        loc = self.ip2location.find_location('194.153.110.160')        
#        self.assertEqual(loc['country_code'], u"TW", msg="Looking up Chung Hwa ip address for Country")
#        self.assertEqual(loc['region'], u"03", msg="Looking up Chung Hwa ip address for Region")
#        self.assertEqual(loc['city'], u"Taipei", msg="Looking up Chung Hwa ip address for City")
#        self.assertEqual(loc['latitude'], '25.0392', msg="Looking up Chung Hwa ip address for Lat")
#        self.assertEqual(loc['longitude'], '121.5250', msg="Looking up Chung Hwa ip address for Lng")
#
#        loc = self.ip2location.find_location('220.229.116.128')
#        self.assertEqual(loc['country_code'], "TW", msg="Looking up paris.fr  ip address for Country")
#        self.assertEqual(loc['region'], "TW", msg="Looking up paris.fr  ip address for Region")
#        self.assertEqual(loc['city'], "TW", msg="Looking up paris.fr  ip address for City")
#        self.assertEqual(loc['postal_code'], "TW", msg="Looking up paris.fr  ip address for Postal Code")
#        self.assertAlmostEqual(float(loc['latitude']), 22.22, msg="Looking up paris.fr  ip address for Lat")
#        self.assertAlmostEqual(float(loc['longitude']), 33.33, msg="Looking up paris.fr  ip address for Lng")
#        self.assertEqual(loc['area_code'], "TW", msg="Looking up paris.fr  ip address for Area")
#        
#
#
#
#
#    def suite():
#        """ Run the test suite. """
#        suite = unittest.TestSuite()     
#        suite.addTest(IPToLocationTest('test_ip_to_country_japan'))        
#        suite.addTest(IPToLocationTest('test_ip_to_country'))        
#        suite.addTest(IPToLocationTest('test_ip_to_location'))        
#        return suite
#
#    @classmethod
#    def tearDown(self):
#        """
#        zip
#        """
#        pass
