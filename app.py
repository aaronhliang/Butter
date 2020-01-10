from flask import Flask, request, render_template
import json
from pymongo import MongoClient
from bson import ObjectId
import requests

app = Flask(__name__)

client = MongoClient("mongodb+srv://suminkim:miknimus@honey-irl-ywt1c.mongodb.net/test?retryWrites=true&w=majority")
honey_db = client['honey_db']

api_key = 'MBjxxSsO'

@app.route('/')
def start():
    return render_template("index.html")


@app.route('/index')
def index():
    return render_template("index.html")

@app.route("/coupons/<coupon_id>", methods=["POST", "GET", "DELETE"])
def couponSpecific(coupon_id):
    # tbd
    url = 'https://api.discountapi.com/v2/deals/' + str(coupon_id)
    result = requests.get(url).json()['deal']
    saved_coupons_collection = honey_db['savedCoupons']

    if(request.method=="DELETE"):
        delete_item = int(coupon_id)
        saved_coupons_collection.delete_one({"id": delete_item})
        return "Coupon deleted"
    elif(request.method=="POST"):
        saved_coupons_collection.insert_one(result)
        api_result = requests.get(url).json()['deal']
        return "Coupon added"
    else:
        url = 'https://api.discountapi.com/v2/deals/' + str(coupon_id)
        result = requests.get(url).json()['deal']
        return render_template("coupon_details.html", coupon=result)

@app.route('/coupons', methods=['GET'])
def coupons():
    results = get_coupons(22101)
    populate_map(results)
    
    return render_template("coupons.html", coupons=results)
        


def get_coupons(zip_code, radius=10):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&radius=' + str(radius) + '&api_key=' + api_key

    return requests.get(url).json()['deals']


def populate_map(coupons):
    for coupon in coupons:
        lat = coupon['deal']['merchant']['latitude']
        lon = coupon['deal']['merchant']['longitude']

        # play around with ur map here

        print("lat:", lat)
        print("longitude: ", lon)
        print()


@app.route('/favorites')
def favorite():
    return render_template("favorites.html")
