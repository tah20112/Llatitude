#!/usr/bin/env python

import serial, time
import speech_recognition as sr
from googleplaces import GooglePlaces, types, lang
import pprint
# from googlemaps import *
# from pygeocoder import Geocoder

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


def get_location_data(locationInput):
    # You may prefer to use the text_search API, instead.
    # query_result = google_places.nearby_search(location=locationInput, radius = 1)
    query_result = google_places.text_search(query=locationInput, radius = 1)

    if query_result.has_attributions:
        print query_result.html_attributions

    coordinates = "" # declare string for retaining lat & lon values

    place = query_result.places[0]
    print place.geo_location
    locationData = (str(place.name) + '|' +
                    str(place.geo_location['lat']) + '|' +
                    str(place.geo_location['lng']))
    # for key in place.geo_location:
    #     coordinates += str(place.geo_location[key]) # keys are unicode, locations are floats

    return locationData

# Get place input from user
# get_places(raw_input('Enter a Location: '))
sydneyData = get_location_data('Los Angelos')
print sydneyData

# print
# results = Geocoder.geocode('Babson College')
# print results
# print results[0].coordinates

# Output to Arduino
ser.write(sydneyData)
# while True: # for testing purposes
# 	print ser.readline() # receive feedback from Arduino
