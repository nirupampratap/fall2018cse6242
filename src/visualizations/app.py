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
    f = open("reviews.json", "r")
    return json.dumps(json.load(f)[business_ID])

@app.route('/similar', methods=['POST'])
def similar():
    business_ID = request.json['data']

    bizidlist = ["_c3ixq9jYKxhLUB0czi0ug", "cKRMmytHxaSt8F0SMEzKqg", "8vA1d9_w4hBjOcrM7mNWFg", "sh69ApUyPhAltAMpv5vX3w", "bVl0_l6sCwjADKRLGxsXAw"]
    simi = {}

    f = open("similar.json", "r")
    return json.dumps(json.load(f)[business_ID])

    """
    attributes, similar_rest = restaurant_case(bizid)
    res = []
    for i in attributes:
        temp = {}
        temp['attributes'] = attributes[i]['attribute'];
        temp['importance'] = attributes[i]['importance'];
        temp['percentage'] = attributes[i]['percentage']
        temp['restaurants'] = []
        attribute = attributes[i]['attribute']
        if attribute in similar_rest:
            for j in similar_rest[attribute]:
                temp_rest = {}
                temp_rest['url'] = similar_rest[attribute][j]['url']
                temp_rest['rating'] = similar_rest[attribute][j]['rating']
                temp_rest['review_count'] = similar_rest[attribute][j]['review_count']
                temp_rest['name'] = similar_rest[attribute][j]['name']
                temp_rest['location'] = similar_rest[attribute][j]['location']
                temp['restaurants'].append(temp_rest)
        res.append(temp)
    simi[bizid] = res
    return pd.Series(res).to_json(orient='values')
    """

if __name__ == '__main__':
	app.run(debug = True)
