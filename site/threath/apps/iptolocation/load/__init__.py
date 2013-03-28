"""
To load all the data  use the project's python prompt, type

from iptolocation.load import load_data
load_data()

drop the tables manually.
db.iptolocation_iprange.drop()
db.iptolocation_country.drop()
db.iptolocation_location.drop()
db.iptolocation_blocks.drop()
"""
import csv
import pdb
from itertools import chain
from os.path import dirname, join
from iptolocation.models import Country, IPRange, Blocks, Location

COUNTRY_FILENAME = join(dirname(__file__), 'GeoIPCountryWhois.csv')
LOCATIONS_FILENAME = join(dirname(__file__), 'GeoLiteCity-Location.csv')
BLOCKS_FILENAME = join(dirname(__file__), 'GeoLiteCity-Blocks.csv')

EXTRA_ROWS = (
    # Private network ranges
    ('10.0.0.0', '10.255.255.255', '167772160', '184549375', 'X1', 'Private Network'),
    ('172.16.0.0', '172.31.255.255', '2886729728', '2887778303', 'X1', 'Private Network'),
    ('192.168.1.1', '192.168.255.255', '3232235520', '3232301055', 'X1', 'Private Network'),
    # Local computer range
    ('127.0.0.0', '127.255.255.255', '2130706432', '2147483647', 'X2', 'Local Computer'),
)

def IsInt( str ):
    """ Is the given string an integer? """
    ok = 1
    try:
        num = int(str)
    except ValueError:
        ok = 0
    return ok
    
def load_data(filename=None, verbose=False):
    #pdb.set-trace()
    countries = {}
    filename = COUNTRY_FILENAME
    reader = csv.reader(open(filename, "rb"))
    # Load new data
    
    for row in chain(reader, EXTRA_ROWS):
        try:
            begin_ip, end_ip, begin_num, end_num, country, name = row
        except ValueError:
            continue
        if country not in countries:
            if verbose:
                print "Creating country:", country, name
            countries[country] = Country.objects.create(code=country, name=name)
        if verbose:
            print "Creating iprange:", begin_num, end_num, countries[country]
        IPRange.objects.create(start=begin_num, end=end_num,
                               country=countries[country])
    
    # now for locations
    filename = LOCATIONS_FILENAME
    reader = csv.reader(open(filename, "rb"))

    for row in chain(reader, EXTRA_ROWS):    # Load new data
        try:
            locId,country,region,city,postalCode,latitude,longitude,metroCode,areaCode = row
        except ValueError:
            continue

        try:
            Location.objects.create(loc_id=locId,
                    country=country,
                    region=region,
                    city=city,
                    postal_code = postalCode,
                    latitude = latitude,
                    longitude = longitude,
                    metro_code = metroCode ,
                    area_code = areaCode )
        except:
            pass
    
    # and now for all the blocks.
    filename = BLOCKS_FILENAME
    reader = csv.reader(open(filename, "rb"))

    locId = "None"
    locations = {}
    for row in chain(reader, EXTRA_ROWS):    # Load new data

        
        startIpNum,endIpNum,locId = row
        try:
            if locId not in locations:
                locations[locId] = Location.objects.filter(loc_id=locId)[0]

            Blocks.objects.create(loc=locations[locId],start = startIpNum,end = endIpNum)
        except:
            pass

