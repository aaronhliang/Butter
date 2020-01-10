from flask import Flask, render_template
import requests
app = Flask(__name__)

api_key = 'MBjxxSsO'


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/coupons', methods=['GET'])
def coupons():
    results = get_coupons(22101)
    return render_template("coupons.html", coupons=results)


def get_coupons(zip_code):
    url = 'https://api.discountapi.com/v2/deals?location=' + str(zip_code) + '&api_key=' + api_key
    return requests.get(url).json()['deals']
