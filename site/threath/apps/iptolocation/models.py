""" 
data from http://www.maxmind.com/app/csv

This is a heavily modified vesion of the original. So much so that 
you cannot replace it with the original.

Getting the ip inside a Django app can be strange. Here is a code snippet.
ip = context['request'].META['REMOTE_ADDR']
try:
    real_ip = context['request'].META['HTTP_X_FORWARDED_FOR']
except KeyError:
    pass
else:
    # HTTP_X_FORWARDED_FOR can be a comma-separated list of IPs. Take just the first one.
    ip = real_ip.split(",")[0]
"""

import pdb
import sys
from django.db import models
from django.db.models.fields import BigIntegerField
try:
    from django.contrib.gis.utils import GeoIP
except:
    pass

class Location(models.Model):
    """ Use IPToCountry & IPToLatLng """

    loc_id      = models.BigIntegerField(default=0)
    country     = models.CharField      (max_length=50, blank=True )
    region      = models.CharField      (max_length=50, blank=True )
    city        = models.CharField      (max_length=50, blank=True )
    postal_code = models.CharField      (max_length=50, blank=True )
    latitude    = models.DecimalField   (max_digits=20, decimal_places=10)
    longitude   = models.DecimalField   (max_digits=20, decimal_places=10)
    metro_code  = models.CharField      (max_length=50, blank=True )
    area_code   = models.CharField      (max_length=50, blank=True )

class Blocks(models.Model):
    loc   = models.ForeignKey(Location)
    start = models.BigIntegerField(default=0)
    end   = models.BigIntegerField(default=0)

class Country(models.Model):
    """ Use IPToCountry & IPToLatLng """

    code = models.CharField(max_length=2, primary_key=True, db_column='cc')
    name = models.CharField(max_length=50, db_column='cn')

    def __unicode__(self):
        """
        Return the readable version of the name.

        For example, "Moldova, Republic of" will return "Republic of Moldova".
        """
        if ', ' not in self.name:
            return self.name
        bits = self.name.split(', ', 1)
        bits.reverse()
        return ' '.join(bits)


class IPRange(models.Model):
    """ depreciated """
    country = models.ForeignKey(Country, db_column='cc')

    start = models.BigIntegerField(default=0)
    end   = models.BigIntegerField(default=0)

    def find_ip(self, ip, catch_errors=True):
        try:
            ret = IPRange.objects.filter(iprange__start__lte=ip).filter(iprange__end__gte=ip)[0]
            return ret
            
        except ObjectDoesNotExist:
            if not catch_errors:
                raise
    def find_country(self, ip):
        try:
            ret = IPRange.objects.filter(iprange__start__lte=ip).filter(iprange__end__gte=ip)[0]
            return ret
            
        except ObjectDoesNotExist:
            raise

class IPToLocation(models.Model):
    """
    
    """
    def find_location(self, ip):
        """
        Pass in a dotted quad. first try the GeoIP db. If not there, fails to the 
        db. This also catches the error in api is installed but settings not correct.
        """

        ret_dict = {}
        try:
            g = GeoIP()
            #g = GeoIP()
            geolocation = g.city(ip)
            ret_dict['latitude'] = str(geolocation['latitude'])
            ret_dict['longitude'] = str(geolocation ['longitude'])
            ret_dict['country_code'] = geolocation['country_code']
            ret_dict['region'] = geolocation['region']
            ret_dict['city'] = geolocation['city']
            return ret_dict
                
        except:
            # didn't work so fall back to the db
            #print "Unexpected error:", sys.exc_info()
            try:
                lip = ip_to_long(ip)
                ret = Blocks.objects.filter(start__lte=lip).filter(end__gte=lip)[0]
                ret_dict['latitude']        = ret.loc.latitude
                ret_dict['longitude']       = ret.loc.longitude
                ret_dict['country_code']    = ret.loc.country
                ret_dict['region']          = ret.loc.region
                ret_dict['city']            = ret.loc.city
                ret_dict['postal_code']     = ret.loc.postal_code
                ret_dict['metro_code']      = ret.loc.metro_code
                ret_dict['area_code']       = ret.loc.area_code
                return ret_dict
            except:
                """ Danger Will Robinson !!!! Just bail. 
                """
                ret_dict['latitude'] = "25.0392"
                ret_dict['longitude'] = "121.5250"
                ret_dict['country_code'] = "TW"
                ret_dict['region'] = "03"
                ret_dict['city'] = "Taipei"
                return ret_dict
    
class IPToCountry(models.Model):
    """ given the IP address will return the two character conuntry id.
        @todo check for the presence of the MaxMind C interface anduse that if availiable 
    """
    
    def find_country_from_ipaddress(self, ipaddress):
        """ Locates country by dotted quad ipaddress"""
        # return "TW" # temp for Sean if not found        
        if ( ipaddress == '127.0.0.1' ) :
            return 'TW'
        long_ip = ip_to_long(ipaddress)
        return self.find_country_from_long(long_ip)

    def find_country_from_long(self, ip):
        """
        Finds a country using the long form of the ip addess
        """        
        
        try:
            ret = IPRange.objects.filter(start__lte=ip).filter(end__gte=ip)[0]
            return ret.country.code
        except:
            return "TW" 

    def get_start_ip(self):
        return long_to_ip(self.start)
    start_ip = property(get_start_ip)

    def get_end_ip(self):
        return long_to_ip(self.end)
    end_ip = property(get_end_ip)


    def __unicode__(self):
        return '%s to %s (%s)' % (self.start_ip, self.end_ip, self.country)

#def ip_to_long(text):
#    pdb.set_trace()
#    w, x, y, z = map(int, text.split('.'))
#    return 6777216*w + 65536*x + 256*y + z # was a type here for some reason , was 16777216

def ip_to_long(ip):
    """
    Convert a IPv4 address into a 32-bit integer.
    
    @param ip: quad-dotted IPv4 address
    @type ip: str
    @return: network byte order 32-bit integer
    @rtype: int
    """
    ip_array = ip.split('.')
    ip_long = long(ip_array[0]) * 16777216 + long(ip_array[1]) * 65536 + long(ip_array[2]) * 256 + long(ip_array[3])
    return ip_long  

def long_to_ip(number):
    number = long(number)
    z = number % 256
    number >>= 8
    y = number % 256
    number >>= 8
    x = number % 256
    number >>= 8
    w = number % 256
    return '%d.%d.%d.%d' % (w, x, y, z)
