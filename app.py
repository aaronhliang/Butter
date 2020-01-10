from flask import Flask, render_template
import requests
app = Flask(__name__)

api_key = 'MBjxxSsO'


@app.route('/')
def start():
    return render_template("index.html")


@app.route('/index')
def index():
    return render_template("index.html")


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
