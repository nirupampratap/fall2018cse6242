from flask import Flask, render_template, request, json
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
	# return getZip(cuisine_list)



	return json.dumps([
		{
			"zipcode": 85007,
			"score":25,
			"attributes":{
				"attr1": 24,
				"attr2": 34,
				"attr3": 6
			},
			"text-review":{
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
			"attributes":{
				"attr1": 10,
				"attr2": 5,
				"attr3": 43
			},
			"text-review":{
				"hello": 2,
				"elephant": 28,
				"car": 51,
				"computer": 24,
				"elevator": 30
			}
		 }
		]
	)

if __name__ == '__main__':
	app.run(debug = True)