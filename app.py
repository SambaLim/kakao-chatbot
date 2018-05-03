
from flask import Flask, request, jsonify

import re
import requests

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
	
	# 구로구 구로3동
	regionCode = '09530540'
	weather, temp = get_weather(regionCode)
	
	dataReceive = request.get_json()
	content = dataReceive['content']
	
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : "안녕하세요."
			}
		}
	return jsonify(dataSend)

# 네이버에서 날씨를 구해오는 방법
def get_weather(regionCode):
	url = "https://m.weather.naver.com/m/main.nhn?regionCode=" + regionCode
	summary_regex = r"weather_set_summary\">(.+?)<br>"
	nowTemp_regex = r"degree_code full\">(.+?)</em>"
	response = requests.get(url)
	data = response.text
	summary = re.search(summary_regex, data)
	nowTemp = re.search(nowTemp_regex, data)
	
	return summary.group(1), nowTemp.group(1)
	
	
if __name__ == '__main__':
	app.run()