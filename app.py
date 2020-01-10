from flask import Flask, request
import json
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb+srv://suminkim:miknimus@honey-irl-ywt1c.mongodb.net/test?retryWrites=true&w=majority")
honey_db = client['honey_db']

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/coupons/<coupon_id>", methods=["POST"])
def favoriteCoupon(coupon_id):
    return coupon_id

