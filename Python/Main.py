#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The first line indicates the program that can execute this script
# The second line encodes utf-8 values and makes them function as strings?

import serial, time
import speech_recognition as sr
from googleplaces import GooglePlaces, types, lang
import pprint
import math
from geopy.distance import vincenty
from urllib2 import urlopen
from contextlib import closing
import json


default_coordinates = (42.293045,-71.264086)    # POE Room coordinates

# Automatically geolocate the connecting IP
def get_sign_coordinates():
    url = 'http://freegeoip.net/json/'  # set the geoip site for querying
    try:
        with closing(urlopen(url)) as response:
            location = json.loads(response.read())  # Get RasPi location data
            print location
            latitude = location['latitude']
            longitude = location['longitude']
            coordinates = (latitude, longitude) # both values are floats
    except:
        coordinates = default_coordinates
    return coordinates

SIGN_COORD = get_sign_coordinates()
gear_ratio = 3

# Begin serial connection with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600) # /dev/ttyACM0 value is in the bottom right of Arduino window
time.sleep(2) # Wait for the Arduino to be ready

# Voices
# obtain audio from the microphone
# r = sr.Recognizer()
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
#     print("Say something!")
#     audio = r.listen(source)

# recognize speech using Google Speech Recognition
# try:
#     # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
#     # instead of `r.recognize_google(audio)`
#     speech = r.recognize_google(audio) # returns voice recording as unicode characters (use str(speech) to convert to string)
# except sr.UnknownValueError:
#     print("Google Speech Recognition could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Speech Recognition service; {0}".format(e))

# google_places = GooglePlaces('AIzaSyB8Yg8zsqZfUwinu2c_V8PP7mgBNrp0h8A')
google_places = GooglePlaces('AIzaSyDNc2X0VlrZPMecga6HDs9RGR_FTJ-26lo')


def get_selected_location_data(locationInput):
    # You may prefer to use the text_search API, instead.
    # query_result = google_places.nearby_search(location=locationInput, radius = 1)
    query_result = google_places.text_search(query=locationInput, radius = 1)

    if query_result.has_attributions:
        print query_result.html_attributions

    place = query_result.places[0]

    return place

def get_distance(location_coord):
    dist = vincenty(SIGN_COORD,location_coord).miles
    return dist

# Get initial bearing toward location using Haversine's method
# Taken from Jeromer's GitHub: https://gist.github.com/jeromer/2005586
def get_angle(location_coord):

    lat1 = math.radians(SIGN_COORD[0])
    lat2 = math.radians(location_coord[0])

    diffLong = math.radians(location_coord[1] - SIGN_COORD[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = ((initial_bearing + 360) % 360)*gear_ratio

    return compass_bearing

# Get place input from user

def get_input():
    data = get_selected_location_data(raw_input('Enter a Location: '))
    distance = get_distance((data.geo_location['lat'], data.geo_location['lng']))
    angle = get_angle((data.geo_location['lat'], data.geo_location['lng']))
    output = str(data.name) + ':' + str(distance) + ':' + str(angle)
    print output
    ser.write(output)
 #   get_input()

get_input()
# Output to Arduino
while True: # for testing purposes
	print ser.readline() # receive feedback from Arduino