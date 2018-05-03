
from flask import Flask, request, jsonify

import time

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
	return 'Hello World!'
'''

nowdate = time.strftime('%y%m%d', time.localtime(time.time()))

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
	today = str(nowdate)
	
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : today,
				"text" : "안녕하세요."
			}
		}
	return jsonify(dataSend)

	
if __name__ == '__main__':
	app.run()