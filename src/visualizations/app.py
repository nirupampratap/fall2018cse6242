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

@app.route('/zip', methods=['GET'])
def zip():
	return json.dumps({
		"yo":1
	})

if __name__ == '__main__':
	app.run(debug = True)