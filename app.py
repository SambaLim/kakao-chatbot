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
	
	# 형태소 분석이 됐는지 확인하기
	word_list = word_extract(content)
	
	# Message 본문
	if content == u"시작하기":
		dataSend = {
			"message" : {
				"text" : hello
			}
		}
	elif word_there(word_list, "날씨")>=1 :
		dataSend = {
			"message" : {
				"text" : winfo
			}
		}
	elif word_there(word_list, "안녕")>=1 :
		dataSend = {
			"message" : {
				"text" : "안녕하세요! 오늘 하루도 맛점하세요!"
			}
		}
	elif word_there(word_list, "점심")>=1 :
		dataSend = {
			"message" : {
				"text" : "점심추천 기능이 추가될 예정이에요! 기대해주세요.\nComming Soon..."
			}
		}
	else :
		dataSend = {
			"message" : {
				"text" : "무슨말인지 잘 모르겠어요 ㅠ_ㅠ"
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

# 문장에서 형태소만을 추출해내는 함수
def word_extract(content):
	# 언어분석 API
	# http://aiopen.etri.re.kr/
	openApiURL = 'http://aiopen.etri.re.kr:8000/WiseNLU'
	accessKey = # 접근 키를 넣어주어야 합니다.
	analysisCode = 'ner'
	word_list = []
	text = str(content)
	requestJson = {
		"access_key" : accessKey,
		"argument" : {
			"text" : text,
			"analysis_code" : analysisCode
		}
	}
	http = urllib3.PoolManager()
	response = http.request(
		"POST",
		openApiURL,
		headers = {"Content-Type":"application/json; charset=UTF-8"},
		body = json.dumps(requestJson)
	)
	dict = json.loads(response.data)
	sentence = dict['return_object']['sentence'][0]['morp']
	for h in sentence:
		word_list.append(str(h['lemma']))
		
	return word_list
	
# 단어 목록에서 특정 단어가 있는지 확인하는 함수 // return 값이 오류가 날 수 있어 변수값으로 바꾸고 진행해볼 것
def word_there(list, word):
	cnt = 0
	for i in range(0, len(list)):
		if list[i]==word:
			cnt = cnt + 1
	return cnt
	
if __name__ == '__main__':
	app.run(debug=True)
	
