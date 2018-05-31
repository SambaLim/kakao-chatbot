from flask import Flask, request, jsonify

import time
import re
import requests
import urllib3
import json
import random

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


app = Flask(__name__)

'''
@app.route('/')
def hello_world():
	return 'Hello World!'
'''

# 입력을 받는 keyboard 부분
@app.route('/keyboard')
def Keyboard():
	
	dataSend = {
		"type" : "buttons",
		"buttons" : ["★ 시작하기", "★ 도움말"]
	}
	return jsonify(dataSend)

# 출력을 하는 message 부분
@app.route('/message', methods=['Post'])
def Message():

	dataReceive = request.get_json()
	content = dataReceive['content']
	user_key = dataReceive['user_key']

	# 리스트 비교용 단어 리스트
	list_thanks = ["고맙", "감사"]
	list_hello = ["안녕", "하이", "헬로"]
	list_eat_Nono = ["안먹", "싫", "먹기싫"]
	list_lunch = ["점심", "메뉴", "뭐먹", "뭐먹을까"]
	list_Yesyes = ["좋", "좋아"]
	list_emo_Nono = ["안좋", "않", "안"]
	list_what_are_you_doing = ["뭐", "하"]
	list_mad = ["나쁘", "화나", "힘들"]
	list_merong = ["메롱", "바보", "멍청이", "멍충이"]
	list_LetsGo = ["콜", "가자"]
	
	# 상태를 정해주는 함수 만들기
	CONVERSATION_START = "시작대화"
	CONVERSATION_NORMAL = "일상대화"
	CONVERSATION_LUNCH = "점심대화"
	CONVERSATION_WEATHER = "날씨대화"
	BUTTON_SETREGION = "지역정하기"
	
	# 형태소 분석한 list 만들기
	word_list = word_extract(content)
	
	# 지역코드  dict
	region_dict = {
			# 특별시, 광역시
			'인천':'11200510',
			'인천광역시':'11200510',
			'인천시':'11200510',
			'서울':'09140550',
			'서울특별시':'09140550',
			'서울시':'09140550',
			'대전':'07170630',
			'대전광역시':'07170630',
			'대전시':'07170630',
			'대구':'06110517',
			'대구광역시':'06110517',
			'대구시':'06110517',
			'부산':'08470690',
			'부산광역시':'08470690',
			'부산시':'08470690',
			'광주':'05140120',
			'광주광역시':'05140120',
			'광주시':'05140120',
			'울산':'10140510',
			'울산광역시':'10140510',
			'울산시':'10140510',
			'세종':'17110250',
			
			# 도
			'경기':'02830410',
			'경기도':'02830410',
			'강원':'01810350',
			'강원도':'01810350',
			'충청북도':'16760370',
			'충북':'16760370',
			'충청남도':'15810320',
			'충남':'15810320',
			'전라북도':'13750360',
			'전북':'13750360',
			'전라남도':'12790330',
			'전남':'12790330',
			'경상북도':'04170400',
			'경북':'04170400',
			'경상남도':'03720415',
			'경남':'03720415',
			'제주도':'14110630',
			'제주':'14110630',

		}
	region_key_list = list(region_dict.keys())
	
	# 첫 인삿말 만들기 
	today = str(nowdate)
	hello = "20" + today[0:2] + "년 " + today[2:4] + "월 " + today[4:6] + "일" + "\n안녕하세요! 오늘 점심뭐먹을까 입니다.\n오늘의 날씨를 알려드릴 수 있고, 점심메뉴를 추천해드릴 수 있어요!" 
	
	# 날씨 정보 출력하기 (지역코드)
	regionCode = Ct2Rc(region_dict, region_key_list, word_list)
	weather, temp = get_weather(regionCode)
	winfo = "오늘의 날씨는 " + str(weather) + "이고,\n온도는 " + str(temp) + "℃ 네요."
	
	# user_key firestore에 저장해보기
	user = db.collection(u'user').document(user_key)
	if first_user(db, user_key) == 0 :
		user.set({
			'state' : CONVERSATION_START
		})
	else :
		user_state = get_user_state(user)
		user.set({
			'state' : user_state
		})
	

	# 재미로 랜덤 점심추천 만들기 (choice1)
	docs = db.collection(u'restaurant').get()
	choice1 = random_menu(docs)
	lunch = "오늘 점심은 " + choice1 + " 어때요?"
	else_lunch = "아니면" + choice1 + " 어때요?"
	
	# Message 본문
	# 초기 버튼 시작하기, 도움말 '★'로 구분
	if content == u"★ 시작하기":
		user.set({
			'state' : CONVERSATION_START
		})
		dataSend = {
			"message" : {
				"text" : hello
			}
		}
	elif content == u"★ 도움말":
		user.set({
			'state' : CONVERSATION_START
		})
		dataSend = {
			"message" : {
				"text" : "Since. 2018.05.03\n점심 메뉴, 음식점 추천을 해주는 챗봇입니다. 오늘의 날씨정보 또한 제공하고 있습니다.\n.\n.\n.\n문의: limsungho07@hanmail.net\nGithub:https://github.com/SambaLim"
			}
		}
		
	# regionCode 테스트
	elif content == "지역코드":
		dataSend = {
			"message" : {
					"type" : "buttons",
					"buttons" : ["★ 시작하기", "★ 도움말"]
			}
		}

	# 일상대화 인사
	elif word_list_there(word_list, list_hello)>=1 :
		user.set({
			'state' : CONVERSATION_NORMAL
		})
		dataSend = {
			"message" : {
				"text" : "안녕하세요! 오늘 기분은 어떠신가요?"
			}
		}
	# 일상대화 나빠, 화나, 등등 부정적인 표현 다루기
	elif word_list_there(word_list, list_mad)>=1 :
		dataSend = {
			"message" : {
				"text" : "천천히 호흡을 가다듬어봐요~ 기분이 한결 좋아질거에요!"
			}
		}
	# 일상대화 나쁜말 정화하기 ^^
	elif word_list_there(word_list, list_merong)>=1 :
		dataSend = {
			"message" : {
				"text" : "바르고 고운말을 사용합시다^^\n문의: limsungho07@hanmail.net"
			}
		}	
	
	# 일상대화 감사표하기
	elif word_list_there(word_list, list_thanks)>=1 :
		dataSend = {
			"message" : {
				"text" : "저야말로 감사합니다!\n필요한 일이 있으면 또 불려주세요!!!"
			}
		}
	# 일상대화 뭐해 대답
	elif word_list_there(word_list, list_what_are_you_doing)>=2 :
		dataSend = {
			"message" : {
				"text" : "너는 지금 뭐해~ 자니~ 밖이야?\n날씨, 점심메뉴를 물어봐주세요~"
			}
		}
		
	# 점심대화 메뉴 추천
	elif word_list_there(word_list, list_lunch)>=1 :
		user.set({
			'state' : CONVERSATION_LUNCH
		})
		if word_list_there(word_list, list_eat_Nono)>=1:
			dataSend = {
				"message" : {
					"text" : "하루의 중심!\n점심은 거르면 안돼요!!!"
				}
			}
		else :
			dataSend = {
				"message" : {
					"text" : lunch
				}
			}
	# 메뉴 긍정에 대한 처리 늘리기
	elif word_list_there(word_list, list_LetsGo)>=1 : 
		if user_state==CONVERSATION_LUNCH :
			if word_list_there(word_list, list_emo_Nono)>=1:
				dataSend = {
					"message" : {
						"text" : else_lunch
					}
				}
			else : 
				dataSend = {
					"message" : {
						"text" : "좋아요!"
					}
				}
		else :
			dataSend = {
				"message" : {
					"text" : "Let's Go!!!"
				}
			}
	
	# 동음이의어 구분하기 "좋아"
	elif word_list_there(word_list, list_Yesyes)>=1 :
		if user_state==CONVERSATION_NORMAL :
			if word_list_there(word_list, list_emo_Nono)>=1:
				dataSend = {
					"message" : {
						"text" : "매운걸 드셔보시는건 어때요?\n스트레스가 날아갈거에요!"
					}
				}
			else : 
				dataSend = {
					"message" : {
						"text" : "저도 기분좋은 하루가 될 것 같아요!"
					}
				}
		elif user_state==CONVERSATION_LUNCH :
			if word_list_there(word_list, list_emo_Nono)>=1 :
				dataSend = {
					"message" : {
						"text" : else_lunch
					}
				}
			else : 
				dataSend = {
					"message" : {
						"text" : "가시죠!!!"
					}
				}
		elif user_state==CONVERSATION_START :
			if word_list_there(word_list, list_emo_Nono)>=1 :
				dataSend = {
					"message" : {
						"text" : "써보시면 좋게될거에요!"
					}
				}
			else : 
				dataSend = {
					"message" : {
						"text" : "좋아요! 저는 점심메뉴추천, 오늘날씨 등을 알고있어요!"
					}
				}
		else :
			dataSend = {
				"message" : {
					"text" : "좋아요!!!"
				}
			}
	# 동음이의어 구분하기 "싫어"
	elif word_list_there(word_list, list_eat_Nono)>=1:
		if user_state==CONVERSATION_LUNCH :
			dataSend = {
				"message" : {
					"text" : else_lunch
				}
			}
		else :
			dataSend = {
				"message" : {
					"text" : "싫으면 시집가세요~"
				}
			}
				
	# 날씨대화 날씨를 알려주는 부분
	elif word_there(word_list, "날씨")>=1 :
		user.set({
			'state' : CONVERSATION_WEATHER
		})
		if word_there(word_list, "내일")>=1 :
			dataSend = {
				"message" : {
					"text" : "저는 오늘의 날씨밖에 알 수 없어요 ㅠ_ㅠ"
				}
			}
		else :
			dataSend = {
				"message" : {
					"text" : winfo
				}
			}
							
	# 모르는 말이 나왔을 때
	else :
		dataSend = {
			"message" : {
				"text" : "무슨말인지 잘 모르겠어요 ㅠ_ㅠ"
			}
		}
		
	return jsonify(dataSend)

# 현재 날짜
nowdate = time.strftime('%y%m%d', time.localtime(time.time()))

# 데이터베이스(firestre) 초기화
cred = credentials.Certificate('first-58ff5b88bb57.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

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
	accessKey = '23dcec62-3fa0-4e1c-8bb4-266ca86ad359'
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
	
# 단어 목록에서 단어 리스트가 있는지 확인하는 함수
def word_list_there(ask_list, ans_list):
	cnt = 0
	for j in range(0, len(ans_list)):
		for i in range(0, len(ask_list)):
			if ans_list[j]==ask_list[i]:
				cnt = cnt + 1
	return cnt
	
# 임의의 메뉴를 선택해주는 함수
def random_menu(docs):
	restaurant_list = []
	for doc in docs:
		string = '{}'.format(doc.id)
		restaurant_list.append(string)
	
	i = random.randint(0, len(restaurant_list)-1)
	choice = restaurant_list[i]
	
	return choice

# User의 상태를 가져오는 함수
def get_user_state(user):
	get_user = user.get()
	dict = get_user.to_dict()
	state = str(dict['state'])
	return state
	
# 처음으로 들어오는 User인지를 확인하는 함수
def first_user(db, user_key):
	user_list = []
	cnt = 0
	docs = db.collection(u'user').get()
	for doc in docs:
		string = '{}'.format(doc.id)
		user_list.append(string)
	
	for i in range(0, len(user_list)):
		if user_list[i] == user_key:
			cnt = cnt + 1
	
	return cnt

# 문자를 지역코드로 바꾸는 함수
def Ct2Rc(region_dict, key_list, word_list):
	cnt = 0
	for i in range(0, len(word_list)):
		for j in range(0, len(key_list)):
			if word_list[i] == key_list[j]:
				cnt = cnt + 1
				region = key_list[j]
	
	if cnt==0:
		# 지역코드가 잘못 입력된 경우 서울의 날씨
		regionCode = '09140550'
		return str(regionCode)
	else :
		regionCode = region_dict[region]
		return str(regionCode)

	
if __name__ == '__main__':
	app.run(debug=True)
	