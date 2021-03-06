#!/usr/bin/env python

import serial, time
import speech_recognition as sr
from googleplaces import GooglePlaces, types, lang
import pprint

# Begin serial connection with Arduino
ser = serial.Serial('/dev/ttyACM0', 9600) # /dev/ttyACM0 value is in the bottom right of Arduino window
time.sleep(2) # Wait for the Arduino to be ready
# Voices
# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Google Speech Recognition
try:
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    speech = r.recognize_google(audio) # returns voice recording as unicode characters (use str(speech) to convert to string)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


# Places
pp = pprint.PrettyPrinter(indent=4)

YOUR_API_KEY = 'AIzaSyB8Yg8zsqZfUwinu2c_V8PP7mgBNrp0h8A'

google_places = GooglePlaces(YOUR_API_KEY)

# You may prefer to use the text_search API, instead.
query_result = google_places.text_search(query=speech, radius = 1)


if query_result.has_attributions:
    print query_result.html_attributions

coordinates = "" # declare string for retaining lat & lon values

place = query_result.places[0]
# Returned places from a query are place summaries.
# pp.pprint(place.name)
# pp.pprint(place.geo_location)
print str(place.name)
for key in place.geo_location:
    coordinates += str(place.geo_location[key]) # keys are unicode, locations are floats

ser.write(coordinates) # Output coordinates to Arduino
while True: # for testing purposes
	print ser.readline() # receive feedback from Arduino
