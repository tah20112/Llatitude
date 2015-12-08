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


# Print data to LED Matrix
def led_print(first_line, second_line):
    pass

# Begin serial connection with Arduino
ser = serial.Serial('/dev/ttyACM1', 9600) # /dev/ttyACM0 value is in the bottom right of Arduino window
time.sleep(2) # Wait for the Arduino to be ready

# Automatically geolocate the connecting IP
# Also, get heading data from the Arduino's magnetometer
def get_sign_data():
    heading = ""
    lines_received = 0
    ser.write('need_heading')
    while len(heading) == 0:
        heading = ser.readline()
    default_coordinates = (42.293045,-71.264086)    # POE Room coordinates
    url = 'http://freegeoip.net/json/'  # set the geoip site for querying
    try:
        with closing(urlopen(url)) as response:
            location = json.loads(response.read())  # Get RasPi location data
            latitude = location['latitude']
            longitude = location['longitude']
            coordinates = (latitude, longitude) # both values are floats
    except:
        coordinates = default_coordinates
    print heading
    return [heading, coordinates]


led_print('Welcome', 'to CoSign')
SIGN_DATA = get_sign_data()
gear_ratio = 3 # We need to update this
led_print('Where do you', 'want to go?')

# Voices
# obtain audio from the microphone
# r = sr.Recognizer()
# with sr.Microphone(sample_rate = 48000, chunk_size = 8192) as source:
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
    query_result = google_places.text_search(query=locationInput, radius = 1)

#    if query_result.has_attributions:
#        print query_result.html_attributions

    place = query_result.places[0]

    return place

def get_distance(location_coord):
    dist = vincenty(SIGN_DATA[1],location_coord).miles
    return dist

# Get initial bearing toward location using Haversine's method
# Taken from Jeromer's GitHub: https://gist.github.com/jeromer/2005586
def get_angle(location_coord):

    lat1 = math.radians(SIGN_DATA[1][0])
    lat2 = math.radians(location_coord[0])

    diffLong = math.radians(float(location_coord[1]) - SIGN_DATA[1][1])

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
    loc_interrupt = False   # Boolean to interrupt listen cycle
    data = get_selected_location_data(raw_input('Enter a Location: '))  # Get user input (must switch for audio)
    distance = get_distance((data.geo_location['lat'], data.geo_location['lng']))   # Calculate distance
    angle = get_angle((data.geo_location['lat'], data.geo_location['lng'])) - float(SIGN_DATA[0])  # Get difference between desired heading and current heading
    led_print(data.name, distance)  # Display location name and relative distance
    ser.write(str(angle))   # Send heading difference to Arduino
    while loc_interrupt == False:   # Wait for Arduino to send new request
        input = ser.readline()     # Record data over serial
        if (input == 'interrupt'):  # Check for interrupt
            loc_interrupt = True
            get_input()     # Repeat process for a new location

get_input()
