
from flask import Flask, request, jsonify

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
	return 'Hello World!'
'''
	
@app.route('/keyboard')
def Keyboard():
	
	dataSend = {
		"type" : "buttons",
		"buttons" : ["시작하기"]
	}
	return jsonify(dataSend)

@app.route('/message', methods=['Post'])
def Message():
	dataReceive = request.get_json()
	content = dataReceive['content']
	
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : "안녕하세요."
			}
		}
	return jsonify(dataSend)



	
if __name__ == '__main__':
	app.run()