#!/usr/bin/python
# -*- coding: utf8 -*-

import requests
import time
from flask import Flask, render_template, request

app = Flask(__name__)


PYMI_LAT, PYMI_LONG = 10.8162109, 106.6941154
RADIUS = 2000
TYPE = "restaurant"
API_KEY = "private-API-key"


@app.route("/")
def index():
    """
    Truy cập website nhập param lat long vào URL:
    e.g: http://127.0.0.1:5000/?lat=51.505&long=-0.09
    """
    restaurants = get_50_restaurants()
    latitude = float(request.args.get("lat", PYMI_LAT))
    longitude = float(request.args.get("long", PYMI_LONG))
    return render_template(
        "index.html", lat=latitude, long=longitude, restaurants=restaurants
    )


def get_request(pagetoken=None):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": "{},{}".format(PYMI_LAT, PYMI_LONG),
        "radius": RADIUS,
        "type": TYPE,
        "pagetoken": pagetoken,
        "key": API_KEY,
    }
    resp = requests.get(url, params=params).json()
    return resp


def get_restaurants(restaurants, resp):
    for item in resp["results"]:
        lat = item.get("geometry").get("location").get("lat")
        lon = item.get("geometry").get("location").get("lng")
        name = item.get("name")
        add = item.get("vicinity")
        restaurants.append(dict(name="{} - {}"
                                .format(name, add), lat=lat, lon=lon))
    return restaurants

def get_50_restaurants():
    restaurants_1 = []
    resp_1 = get_request()
    restaurants_2 = get_restaurants(restaurants_1, resp_1)
    pagetoken_1 = resp_1.get("next_page_token")
    time.sleep(10)
    resp_2 = get_request(pagetoken=pagetoken_1)
    restaurants_3 = get_restaurants(restaurants_2, resp_2)
    pagetoken_2 = resp_2.get("next_page_token")
    time.sleep(10)
    resp_3 = get_request(pagetoken=pagetoken_2)
    restaurants = get_restaurants(restaurants_3, resp_3)
    return restaurants[:50]


if __name__ == "__main__":
    app.run(debug=True)
