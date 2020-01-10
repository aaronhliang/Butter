import googlemaps
import pprint
import time
import geocoder

from GoogleMapsAPIKey import get_my_key
#
# #define API key
API_KEY = get_my_key()
#
# #define our client
gmaps = googlemaps.Client(key = API_KEY)

def getCurrentLocation():

    myloc = geocoder.ip('me')
    myloc = myloc.latlng

    return myloc

