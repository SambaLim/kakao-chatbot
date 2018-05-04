# 카카오톡 챗봇

> 기존에 있던 Telegram 챗봇을 카카오톡으로 옮겨보려고 합니다.<br>
> 인공지능 음식 추천을 목표로 하고 있습니다. 

**heroku 주소**<br>
https://immense-springs-10641.herokuapp.com/<br>
https://git.heroku.com/immense-springs-10641.git<br>
immense-springs-10641

----------
## 01. Flask
1. virtualenv
    pip install virtualenv
2. 폴더생성
    mkdir 폴더이름
    cd 폴더이름
3. app.py 생성
- power-shell
    new-item app.py
- 내용
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello World!'
    
    if __name__ == '__main__':
        app.run()
4.  flask 확인
    python app.py


----------
## 02. Virtualenv 설정
1. virtualenv 설정
    pip install numpy
    virtualenv venv
    cd venv/Scripts
    .\activate
2. 필수 패키지 설치
    pip install flask gunicorn jinja2
3. Procfile 만들기 (Power-Shell)
    new-item Procfile
- 내용
    web: gunicorn app:app


----------
## 03. Requirements 만들기
1. 생성
    pip freeze requirements
    pip freeze > requirements.txt
2. Encoding 방식 바꾸기
  메모장으로 requirements.txt를 들어가서 `다른이름으로 저장하기`를 통해 ANSI로 저장함


----------
## 04. Heroku에 Deploy
1. gitignore 생성 (Power-Shell)
    new-item .gitignore
2. git 시작하기
    git init
    git add --all
    git commit -m "commit"
3. heroku 접속
    heroku login
    heroku create
    git remote -v
    heroku  https://git.heroku.com/polar-tor-1665.git (fetch)
    heroku  https://git.heroku.com/polar-tor-1665.git (push)
    git push heroku master
4. 연결 확인

`https://polar-tor-1665.herokuapp.com/`

5. 로그 태일
    heroku logs --tail -a immense-springs-10641
