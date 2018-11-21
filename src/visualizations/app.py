from flask import Flask, render_template, request, json
from getLoc import get_locations

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
	return json.dumps(get_locations(cuisine_list))
	"""
	return json.dumps([
		{
			"zipcode": 85007,
			"score":25,
			"attr":{
				"attr1": 24,
				"attr2": 34,
				"attr3": 6
			},
			"textReview":{
				"hello": 23,
				"elephant": 45,
				"car": 6,
				"computer": 10,
				"elevator": 15
			}
		 },
		 {
			"zipcode": 85009,
			"score":78,
			"attr":{
				"attr1": 10,
				"attr2": 5,
				"attr3": 43
			},
			"textReview":{
				"hello": 2,
				"elephant": 28,
				"car": 51,
				"computer": 24,
				"elevator": 30
			}
		 },
		 {
			"zipcode": 85014,
			"score":56,
			"attr":{
				"attr1": 28,
				"attr2": 79,
				"attr3": 33
			},
			"textReview":{
				"hello": 2,
				"elephant": 28,
				"car": 51,
				"computer": 24,
				"elevator": 30,
				"banane": 2,
				"kiwi": 28,
				"poire": 51,
				"peche": 24,
				"ananas": 30,
				"avocat": 2,
				"pomme": 28,
				"mandarine": 51,
				"mangue": 24,
				"figue": 30
			}
		 }
		]
	)
	"""

@app.route('/find_improve', methods=['POST'])
def review():
    business_ID = request.json['data']
    #return get_review(business_ID)

    return json.dumps([
                       {
                       'attribute': 'Delivery',
                       'importance': 5,
                       'percentage': '100%',
                       'restaurants':[
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '123'
                                      },
                                      
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '123'
                                      },
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '123'
                                      }
                                      ]
                       },
                       
                       {
                       'attribute': 'Parking',
                       'importance': 4,
                       'percentage': '95%',
                       'restaurants':[
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '123'
                                      },
                                      
                                      {
                                      'location': 123,
                                      'name': 'john papa',
                                      'ratings': 3.6,
                                      'price': '123'
                                      },
                                      {
                                      'location': 123,
                                      'name': 'pizza',
                                      'ratings': 3.6,
                                      'price': '123'
                                      }
                                      ]
                       },
                       
                       {
                       'attribute': 'Takeout',
                       'importance': 3,
                       'percentage': '30%',
                       'restaurants':[
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '$$$'
                                      },
                                      
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '$$'
                                      },
                                      {
                                      'location': 123,
                                      'name': 'randon',
                                      'ratings': 3.6,
                                      'price': '12$3'
                                      }
                                      ]
                       }
                       ])

if __name__ == '__main__':
	app.run(debug = True)
