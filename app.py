from flask import Flask, request, jsonify

import time
import re
import requests

app = Flask(__name__)

'''
@app.route('/')
def hello_world():
	return 'Hello World!'
'''

nowdate = time.strftime('%y%m%d', time.localtime(time.time()))

# 입력을 받는 keyboard 부분
@app.route('/keyboard')
def Keyboard():
	
	dataSend = {
		"type" : "buttons",
		"buttons" : ["시작하기"]
	}
	return jsonify(dataSend)

# 출력을 하는 message 부분
@app.route('/message', methods=['Post'])
def Message():

	def get_weather(regionCode):
		url = "https://m.weather.naver.com/m/main.nhn?regionCode=" + regionCode
		summary_regex = r"weather_set_summary\">(.+?)<br>"
		nowTemp_regex = r"degree_code full\">(.+?)</em>"
		response = requests.get(url)
		data = response.text
		summary = re.search(summary_regex, data)
		nowTemp = re.search(nowTemp_regex, data)
	
		return summary.group(1), nowTemp.group(1)

	dataReceive = request.get_json()
	content = dataReceive['content']
	
	# 첫 인삿말 만들기
	today = str(nowdate)
	hello = today + "\n안녕하세요! 오늘 점심뭐먹을까 입니다.\n점심 음식점, 메뉴 걱정말고 저에게 맡겨주세요!" 
	
	# 날씨 정보 출력하기
	regionCode = "09530540"
	weather, temp = get_weather(regionCode)
	winfo = "오늘 날씨는 " + str(weather) + "이고, 온도는" + str(temp) + "℃ 입니다. \n오늘의 날씨는 메뉴를 선택하는데 영향을 미칩니다!" 
	
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : hello
			}
		}
	elif content == u"날씨":
		dataSend = {
			"message" : {
				"text" : winfo
			}
		}
	return jsonify(dataSend)

	
if __name__ == '__main__':
	app.run()