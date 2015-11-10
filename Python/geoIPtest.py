#!/usr/bin/env python 
from urllib2 import urlopen
from contextlib import closing
import json

# Automatically geolocate the connecting IP
url = 'http://freegeoip.net/json/'
try:
    with closing(urlopen(url)) as response:
        location = json.loads(response.read())
        print location
        latitude = location['latitude']
        longitude = location['longitude']
        print latitude, longitude # both values are floats
        # city = location['city'] # Additional options from location
        # state = location['region_name']
        # country = location['country_name']
        # zip_code = location['zipcode']
except:
    COORD = default_coordinates