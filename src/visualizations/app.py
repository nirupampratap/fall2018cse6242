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

if __name__ == '__main__':
	app.run(debug = True)