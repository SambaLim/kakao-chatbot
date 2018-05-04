# 카카오톡 챗봇

> 기존에 있던 Telegram 챗봇을 카카오톡으로 옮겨보려고함.
> 인공지능 음식 추천을 목표로 하고 있습니다. 

**kakaobot**
https://immense-springs-10641.herokuapp.com/
https://git.heroku.com/immense-springs-10641.git
immense-springs-10641

----------
## 01. Flask
1. virtualenv
    > pip install virtualenv
2. 폴더생성
    > mkdir 폴더이름
    > cd 폴더이름
3. app.py 생성
- power-shell
    > new-item app.py
- 내용
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'
    
    if __name__ == '__main__':
        app.run()
4.  flask 확인
    > python app.py


----------
## 02. Virtualenv 설정
1. virtualenv 설정
    > pip install numpy
    > virtualenv venv
    > cd venv/Scripts
    > .\activate
2. 필수 패키지 설치
    > pip install flask gunicorn jinja2
3. Procfile 만들기 (Power-Shell)
    > new-item Procfile
- 내용
    web: gunicorn app:app


----------
## 03. Requirements 만들기
1. 생성
    > pip freeze requirements
    > pip freeze > requirements.txt
2. Encoding 방식 바꾸기
  메모장으로 requirements.txt를 들어가서 `다른이름으로 저장하기`를 통해 ANSI로 저장함


----------
## 04. Heroku에 Deploy
1. gitignore 생성 (Power-Shell)
    > new-item .gitignore
2. git 시작하기
    > git init
    > git add --all
    > git commit -m "commit"
3. heroku 접속
    > heroku login
    > heroku create
    > git remote -v
    heroku  https://git.heroku.com/polar-tor-1665.git (fetch)
    heroku  https://git.heroku.com/polar-tor-1665.git (push)
    # 여기서 나오는 두 주소를 저장해 둡니다.
    > git push heroku master
4. 연결 확인

`https://polar-tor-1665.herokuapp.com/`

5. 로그 태일
    > heroku logs --tail -a immense-springs-10641


----------
## 99. 참조링크
- http://lambda2.tistory.com/1
- 홍익대학교 학식알리미 : 
  https://m.blog.naver.com/PostView.nhn?blogId=wintermy201&logNo=220759780706&proxyReferer=https%3A%2F%2Fwww.google.co.kr%2F
- https://github.com/plusfriend/auto_reply
- pipenv 시작 :
  https://cjh5414.github.io/how-to-manage-python-project-with-pipenv/
- flask : http://flask.pocoo.org/docs/1.0/quickstart/
- heroku : https://www.heroku.com/
- heroku 배포 : http://jacegem.github.io/blog/2018/%EC%B9%B4%EC%B9%B4%EC%98%A4%ED%86%A1%20%ED%94%8C%EB%9F%AC%EC%8A%A4%EC%B9%9C%EA%B5%AC%20%EC%8A%A4%EB%A7%88%ED%8A%B8%EC%B1%84%ED%8C%85%20%EB%A7%8C%EB%93%A4%EA%B8%B0%208%20-%20Heroku%20%EB%B0%B0%ED%8F%AC/
- 설명 : https://github.com/plusfriend/auto_reply
- flask + heroku : http://www.gtlambert.com/blog/deploy-flask-app-to-heroku

