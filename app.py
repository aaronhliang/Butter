from flask import Flask, render_template
import requests
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from GoogleMapsAPIKey import get_my_key
from Maps import getCurrentLocation

app = Flask(__name__)

api_key = 'MBjxxSsO'

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = get_my_key()

# Initialize the extension
GoogleMaps(app)

@app.route('/')
def start():
    return render_template("index.html")


@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/coupons', methods=['GET'])
def coupons():
    results = get_coupons(22101)
    print(results)
    return render_template("coupons.html", coupons=results)

def get_coupons(zip_code, radius = 10):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&radius=' + str(radius) + '&api_key=' + api_key
    return requests.get(url).json()['deals']

@app.route("/map")
def mapview():

    currentLocation = getCurrentLocation()
    coupons = get_coupons(22101)
    markers = populate_map(coupons)

    sndmap = Map(
        identifier="sndmap",
        lat=38.900060,
        lng=-76.995700,
        markers=markers,
        style="height:500px;width:500px;margin:0;",
        zoom = 18
    )
    return render_template('Map.html', sndmap=sndmap)

def populate_map(coupons):
    markers = []
    for coupon in coupons:
        lat = coupon['deal']['merchant']['latitude']
        lon = coupon['deal']['merchant']['longitude']
        title = coupon['deal']['short_title']
        terms = coupon['deal']['fine_print']
        markers.append(
            {
                'lat': lat,
                'lng': lon,
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'infobox': "<div><h3>" + title + " </h3><p>" + terms + "</div>"
            }
        )

    return markers


def get_coupons(zip_code, radius=10):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&radius=' + str(radius) + '&api_key=' + api_key

    return requests.get(url).json()['deals']


@app.route('/favorites')
def favorite():
    return render_template("favorites.html")