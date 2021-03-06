from flask import Flask, request, render_template
import json
from pymongo import MongoClient
from bson import ObjectId
import requests
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from GoogleMapsAPIKey import get_my_key
from Maps import getCurrentLocation, getZipCode

app = Flask(__name__)

client = MongoClient("mongodb+srv://suminkim:miknimus@honey-irl-ywt1c.mongodb.net/test?retryWrites=true&w=majority")
honey_db = client['honey_db']

# you can set key as config
app.config['GOOGLEMAPS_KEY'] = get_my_key()

# Initialize the extension
GoogleMaps(app)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@app.route('/')
def start():
    return render_template("index.html")


api_key = "MBjxxSsO"


@app.route('/index')
def index():
    return render_template("index.html")


@app.route("/coupons/<coupon_id>", methods=["POST", "GET", "DELETE"])
def couponSpecific(coupon_id):
    # tbd
    url = 'https://api.discountapi.com/v2/deals/' + str(coupon_id)
    result = requests.get(url).json()['deal']
    saved_coupons_collection = honey_db['savedCoupons']

    if(request.method == "DELETE"):
        delete_item = int(coupon_id)
        saved_coupons_collection.delete_one({"id": delete_item})
        return "Coupon deleted"
    elif(request.method == "POST"):
        saved_coupons_collection.insert_one(result)
        api_result = requests.get(url).json()['deal']
        return "Coupon added"
    else:
        url = 'https://api.discountapi.com/v2/deals/' + str(coupon_id)
        result = requests.get(url).json()['deal']
        return render_template("coupon_details.html", coupon=result)

@app.route("/favorites", methods=["GET"])
def favoritedCoupons():
    saved_coupons_collection = honey_db['savedCoupons']
    allFavs1 = list(saved_coupons_collection.find())

    # allFavs = JSONEncoder().encode(list(saved_coupons_collection.find()))
    # saved_coupons_collection.find()

    return render_template("favorites.html", coupons=allFavs1)


@app.route('/coupons', methods=['GET'])
def coupons():
    # results = get_coupons(getZipCode()) #uncomment for location tracking
    results = get_coupons(22101) # hardcoded in for zip code

    return render_template("coupons.html", coupons=results)


def get_coupons(zip_code, radius=10):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&radius=' + str(radius) + '&api_key=' + api_key
    return requests.get(url).json()['deals']


@app.route("/map")
def mapview():

    currentLocation = getCurrentLocation()
    #Uncomment this line to track location
    # coupons = get_coupons(getZipCode())
    coupons = get_coupons(22101) # hardcoded in zip code for demo purposes
    markers = populate_map(coupons, currentLocation)

    sndmap = Map(
        identifier="sndmap",
        lat=38.900060,
        lng=-76.995700,
        markers=markers,
        style="height:500px;width:100%;margin:0;",
        zoom=18
    )

    # Uncomment for location tracking
    # sndmap = Map(
    #     identifier="sndmap",
    #     lat=currentLocation[0],
    #     lng=currentLocation[1],
    #     markers=markers,
    #     style="height:500px;width:100%;margin:0;",
    #     zoom=20
    # )

    return render_template('Map.html', sndmap=sndmap)


def populate_map(coupons, currentLocation):
    markers = []
    for coupon in coupons:
        couponId = str(coupon['deal']['id'])
        lat = coupon['deal']['merchant']['latitude']
        lon = coupon['deal']['merchant']['longitude']
        title = coupon['deal']['short_title']
        terms = coupon['deal']['fine_print']
        markers.append(
            {
                'lat': lat,
                'lng': lon,
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'infobox': "<div><h3><a href=/coupons#" + couponId + ">" + title + "</a></h3><p>" + terms + "</div>"
            }
        )

        markers.append(
            {
                'lat': 38.900055,
                'lng': -76.995700,
                'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                'infobox': "You are here"
            }
        )

        # markers.append(
        #     {
        #         'lat': currentLocation[0],
        #         'lng': currentLocation[1],
        #         'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        #         'infobox': "You are here"
        #     }
        # )

    return markers


def get_coupons(zip_code, radius=10):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&radius=' + str(radius) + '&api_key=' + api_key

    return requests.get(url).json()['deals']
