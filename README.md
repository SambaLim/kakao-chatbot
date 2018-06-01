# 카카오톡 플러스 친구 챗봇

> 카카오톡 플러스 친구 챗봇을 만드는 방법을 github를 통해 공개합니다.
> 카카오톡 플러스 친구에서 ‘오늘 점심뭐먹을까’를 검색하시면 챗봇을 사용해 볼 수 있습니다.
> ‘오늘 점심뭐먹을까’는 점심메뉴 추천과 날씨정보 제공을 할 수 있습니다.


# 01. 개요
> 어떤 챗봇을 무엇으로 만들 것인지 알아봅니다.


- 어떤 챗봇을 만들 것인가?
  - 점심메뉴 추천
  - 날씨정보 제공


- 무엇으로 만들 것인가?
  - 메신져 : 카카오톡 플러스 친구
  - 프레임워크 : Flask
  - 언어 : Python
  - 서버 : Heroku
  - DB : FireStore


----------
# 02. 설계
> 업무 프로세스와 스크립트로 나누어 간단한 설계를 해봅니다.


- 업무 프로세스
  - 안내
  
User  : 1시작 → 2도움말 선택

Bot   : 3도움말 목록 중 선택한 항목 안내(단어, 스크립트)


  - 메뉴 추천
  
User : 1점심 메뉴에 대한 의문 -> 3긍정/부정

Bot  : 2점심메뉴 추천 -> 4확인/재추천

  - 날씨 정보
  
User : 1날씨에 대한 의문

Bot  : 2날씨정보 제공



- 스크립트
  - 일상 대화
  
    User: 안녕^^
    
    Bot: 안녕하세요! 오늘 기분은 어떠신가요?
    
    User: 나빠 ㅠ_ㅠ
    
    Bot: 천천히 호흡을 가다듬어봐요~ 기분이 한결 좋아질거에요!
    
  - 점심 대화
  
    User: 뭐먹을까?
    
    Bot: 오늘 점심은 돈까스 어때요?
    
    User: 싫어
    
    Bot: 아니면 국밥 어때요?
    
    User:ㅇㅇ
    
    Bot: 가시죠!!!
    
  - 날씨 대화
  
    User: 오늘 제주 날씨 어때?
    
    Bot: 오늘 날씨는 맑음 이고, 온도는 21℃ 네요.
    


----------
# 03. 개발환경 설정
> 챗봇을 만들기 앞서서 Flask, FireStore, Heroku를 설치하여 개발환경을 설정합니다.
> Git / Anaconda 4.5.2 / Python 3.6.4 를 사용하였습니다.
> 각각 참조한 사이트는 99. 참조링크에 정리해두었습니다.


- Flask
  - Anaconda Prompt에서 아래의 코드를 입력하여 Flask를 설치합니다.
  
    ```$ pip install Flask```


  - 설치 완료 후, 가장 최근의 Flask Code를 사용하고 싶다면 아래의 코드를 입력합니다.
  
    ```$ pip install -U https://github.com/pallets/flask/archive/master.tar.gz```


  - 원하는 경로에 폴더를 생성합니다.
  
    ```$ mkdir KakaoBot```


  - 해당 폴더 내에 `app.py` 파일을 생성하고 다음과 같은 코드를 입력합니다.
  ```
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'
    
    if __name__ == '__main__':
        app.run()
    ```

  - Anaconda Prompt 에서 Flask가 실행되는지 확인합니다.
    python app.py

- FireStore
  - 아래의 주소를 입력하여 Firebase 콘솔을 열고 새 프로젝트를 만들어줍니다.
  
    ```https://console.firebase.google.com/?hl=ko```


  - Anaconda Prompt 에서 firebase를 설치합니다.
  
    ```pip install --upgrade firebase-admin```


  - 앞서 만들었던 app.py에 아래와 같은 코드를 추가합니다.
  ```
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import firestore
    
    # Use a service account
    cred = credentials.Certificate('path/to/serviceAccount.json')
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
   ```

`**path/to/serviceAccount.json**`을 얻기 위해서는 Cloud Platform 콘솔에서 [**IAM 및 관리자 > 서비스 계정**](https://console.cloud.google.com/iam-admin/serviceaccounts?hl=ko)으로 이동해야 합니다. (99. 참조링크 / Firebase 시작 참고)


- Heroku
  - AnacondaPrompt에서 필수 패키지를 다운받습니다.
  
    ```$ pip install flask gunicorn jinja2```


  - 앞서 app.py를 생성했던 폴더내에 `Procfile` 을 생성 합니다.
  
    ```$ new-item Procfile```


  - Procfile내에 아래의 코드를 삽입합니다.
  
    ```web: gunicorn app:app```


  - requirements.txt 를 생성하고 패키지들을 옮겨줍니다.
  ```
    $ pip freeze requirements
    $ pip freeze > requirements.txt
  ```

  - git을 이용해 heroku에 deploy 합니다.
  ```
    $ git init
    $ git add *
    $ git commit -m "first_commit"
    $ heroku login
    $ heroku create
    $ git push heroku master 
  ```

- 플러스친구 관리자
  - 플러스친구 관리자 센터에 로그인을 합니다.
  - 플러스 친구를 생성합니다.
  - 스마트 채팅 → API 형 선택
  - 앱 URL에 heroku에 배포한 URL을 등록합니다.


----------
# 04. Data 가져오기 & API
> 날씨 정보 연동은 네이버 날씨를 파싱하여 처리하였습니다.
> 언어 분석은 엑소브레인에서 제공하는  Open API 서비스를 사용하였습니다.


- 날씨 정보 연동
  - 지역코드(regionCode)는 직접 검색을 통해 알아냈습니다.
    (app.py내에 region_dict라는 이름의 딕셔너리로 정리되어있습니다.)


  - 필수 패키지 설치 (Anaconda Prompt)
  
    ```$ pip install re requests```


  - 날씨, 온도 가져오기
    `app.py`의 `get_weather` 함수를 참고합니다.


- 언어 분석
  - 엑소브레인 사이트에서 Open API 사용신청을 하여 API 키를 발급받습니다.
    (1일~3일 정도 소요됩니다.)


  - 기본설정은 99. 참조링크의 언어분석 개발가이드를 참고합니다.


  - `app.py`의 `word_extract` 함수를 참고합니다.


----------
# 05. 구현
- 업데이트 예정입니다.





----------
# 99. 참조링크
- Git 다운로드:
  https://git-scm.com/downloads
- Anaconda 다운로드:
  https://www.anaconda.com/download/
- Flask 설치:
  http://flask.pocoo.org/docs/1.0/installation/#installation
- FireStore 시작 :
  https://firebase.google.com/docs/firestore/quickstart?hl=ko
- heroku 설치 & deploy :
  http://www.gtlambert.com/blog/deploy-flask-app-to-heroku
- heroku 연동:
  [http://jacegem.github.io/blog/2018/카카오톡 플러스친구 스마트채팅 만들기 8 - Heroku 배포/](http://jacegem.github.io/blog/2018/카카오톡 플러스친구 스마트채팅 만들기 8 - Heroku 배포/)
- 플러스 친구 관리자 페이지 :
  https://center-pf.kakao.com/login
- 날씨정보 연동 :
  https://www.clien.net/service/board/lecture/11211399
- 엑소브레인 오픈 API :
  http://exobrain.kr/quest/externalService.do
- 언어분석 개발가이드 :
  http://aiopen.etri.re.kr/doc_language.php
- 구현 참고 :
  https://github.com/plusfriend/auto_reply

