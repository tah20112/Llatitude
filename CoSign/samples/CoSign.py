#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The first line indicates the program that can execute this script
# The second line encodes utf-8 values and makes them function as strings?

import serial, time, pprint, math, json, threading
import speech_recognition as sr
from googleplaces import GooglePlaces, types, lang
from geopy.distance import vincenty
from urllib2 import urlopen
from contextlib import closing
from runtext import RunText



#################### Global Variables ######################
# google_places = GooglePlaces('AIzaSyB8Yg8zsqZfUwinu2c_V8PP7mgBNrp0h8A')
google_places = GooglePlaces('AIzaSyDNc2X0VlrZPMecga6HDs9RGR_FTJ-26lo')
SIGN_DATA = []
GEAR_RATIO = 3 # We need to update this

#################### Helper Functions ######################

def led_print(firstLine, secondLine, stop):
    """Print data to LED Matrix, only call using threading"""
    parser = RunText(firstLine, secondLine, stop)
    if (not parser.process()):
        parser.print_help()

def get_distance(location_coord):
    dist = vincenty(SIGN_DATA[1],location_coord).miles
    return dist

def get_angle(location_coord):
    """
    Get initial bearing toward location using Haversine's method
    Taken from Jeromer's GitHub: https://gist.github.com/jeromer/2005586
    """
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
    compass_bearing = ((initial_bearing + 360) % 360) * GEAR_RATIO

    return compass_bearing

def get_selected_location_data(locationInput):
    query_result = google_places.text_search(query=locationInput, radius = 1)
    print 'places:',query_result.places
    try:
        return query_result.places[0]
    except IndexError:
        return get_selected_location_data('Boston')

#################### STARTUP THREAD ######################
def display_loading(stop):
    led_print('CoSign', '0', stop)

def setup():
    """Setup the arduino and our current location & direction"""
    global SIGN_DATA
    global arduino

    # Begin serial connection with Arduino, wait for it to be ready
    arduino = serial.Serial('/dev/ttyACM0', 9600)
    time.sleep(2)
    print 'connected to arduino'

    # Get heading data from the Arduino's magnetometer
    heading = ""
    arduino.write('need_heading')
    print 'trying to get heading from arduino...'
    while len(heading) == 0:
        heading = arduino.readline()
    print 'got heading:',heading

    # Find our location using geoIP
    try:
        # Query the geoip site
        with closing(urlopen('http://freegeoip.net/json/')) as response:
            location = json.loads(response.read())
            latitude = location['latitude']
            longitude = location['longitude']
            # Both values are floats
            coordinates = (latitude, longitude)
    except:
        # Can't find our location, so default to the POE room
        coordinates = (42.293045,-71.264086)
    print 'got coordinates:',coordinates

    SIGN_DATA = [heading, coordinates]

#################### WAITING FOR BUTTON THREAD ######################

def display_waiting(stop):
    led_print('Press the Button', '0', stop)

def wait_for_arduino_button():
    """Stays in this loop until the button is pressed"""
    # while buttonPressed == False:
    print 'waiting for button....'
    while True:
        # Wait for Arduino to tell us the button was pressed
        if ('interrupt' in arduino.readline()):
            # Button was pressed
            # buttonPressed = True
            print 'button pressed'
            return
            # get_input() # Repeat process for a new location

#################### LISTENING & CALCULATING THREAD ######################

def display_listening(stop):
    led_print('Listening...','0', stop)

def get_input_and_calculate():
    global NAME
    global DISTANCE
    global ANGLE

    #TODO change this for microphone:
    NAME = raw_input('Enter a Location: ')

    data = get_selected_location_data(NAME)
    lat = data.geo_location['lat']
    lng = data.geo_location['lng']

    # Calculate distance
    DISTANCE = get_distance((lat, lng))
    print 'got distance:',DISTANCE

    # Get difference between desired heading and current heading
    ANGLE = get_angle((lat, lng)) - float(SIGN_DATA[0])
    print 'got angle:',ANGLE

#################### OUTPUT THREAD ######################

def display_place(stop):
    led_print(NAME, DISTANCE, stop)
    print 'printed name & distance to LED'

def send_angle_to_arduino():
    arduino.write(str(ANGLE))   # Send heading difference to Arduino
    print 'angle sent to arduino'

    #TODO wait until motor finishes pointing?

#################### MAIN PROGRAM ######################

def MAIN():
    thread_functions(display_loading, setup)
    print 'SETUP THREAD DONE'
    thread_functions(display_waiting, wait_for_arduino_button)
    while True:
        thread_functions(display_listening, get_input_and_calculate)
        thread_functions(display_place, send_angle_to_arduino)
        thread_functions(display_place, wait_for_arduino_button)

def thread_functions(display_func, process_func):
    displayStop = threading.Event()
    displayThread = threading.Thread(target=display_func, args=(displayStop,))
    displayThread.daemon = True
    displayThread.start()
    
    processThread = threading.Thread(target=process_func)
    processThread.daemon = True
    processThread.start()

    # Wait for the process to finish
    processThread.join()
    # Stop the display thread
    displayStop.set()
    time.sleep(2)

MAIN()
