from flask import Flask, request, jsonify

import time
import re
import requests
import urllib3
import json


app = Flask(__name__)

'''
@app.route('/')
def hello_world():
	return 'Hello World!'
'''

# 현재 날짜
nowdate = time.strftime('%y%m%d', time.localtime(time.time()))

# 언어분석 API
# http://aiopen.etri.re.kr/
openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
accessKey = "23dcec62-3fa0-4e1c-8bb4-266ca86ad359"
analysisCode = "ner"

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

	dataReceive = request.get_json()
	content = dataReceive['content']
	
	# 첫 인삿말 만들기
	today = str(nowdate)
	hello = "20" + today[0:2] + "년 " + today[2:4] + "월 " + today[4:6] + "일" + "\n안녕하세요! 오늘 점심뭐먹을까 입니다.\n점심 음식점, 메뉴 걱정말고 저에게 맡겨주세요!" 
	
	# 날씨 정보 출력하기
	regionCode = "09530540"
	weather, temp = get_weather(regionCode)
	winfo = "오늘의 날씨는 " + str(weather) + "이고,\n온도는 " + str(temp) + "℃ 네요."
	
	# 언어분석 json
	requestJson = {
		"accessKey" : accessKey,
		"argument" : {
			"text" : content,
			"analysis_code" : analysisCode
		}
	}
	http = urllib3.PoolManager()
	response = http.request(
		"POST",
		openApiURL,
		headers = {"Content-Type":"application/json; charset=UTF-8"},
		body = json.dumps(requestJson).encode('utf-8')
	)
	dict = json.loads(response.data)
	strmsg = dict['return_object']['sentence'][0]['morp']

	# Message 본문
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : hello
			}
		}
	elif content == u"날씨" :
		dataSend = {
			"message" : {
				"text" : winfo
			}
		}
	return jsonify(dataSend)


# 지역의 날씨와 온도를 가져오는 함수	
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
	app.run(debug=True)