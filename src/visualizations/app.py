from flask import Flask, render_template, request, json
from getLoc import get_locations
from reviews import getReviews
from attributes import restaurant_case
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/launch')
def launch():
	return render_template('launch.html')

@app.route('/improve')
def improve():
	return render_template('improve.html')

@app.route('/zip', methods=['POST'])
def zip():
	cuisine_list = request.json["data"]
	return get_locations(json.dumps(cuisine_list)).to_json()
	

@app.route('/find_improve', methods=['POST'])
def review():
    business_ID = request.json['data']
    return json.dumps(getReviews(business_ID, 3))

@app.route('/similar', methods=['POST'])
def similar():
    business_ID = request.json['data']
    res = restaurant_case("Oh_mShbdmaoRX8iZVdE0vw")
    return res

if __name__ == '__main__':
	app.run(debug = True)
