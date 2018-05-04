# 카카오톡 챗봇

> 기존에 있던 Telegram 챗봇을 카카오톡으로 옮겨보려고 합니다.<br>
> 인공지능 음식 추천을 목표로 하고 있습니다. 

**heroku 주소**<br>
https://immense-springs-10641.herokuapp.com/<br>
https://git.heroku.com/immense-springs-10641.git<br>
immense-springs-10641

----------
## 01. Flask
1. virtualenv<br>
    pip install virtualenv<br>
2. 폴더생성<br>
    mkdir 폴더이름<br>
    cd 폴더이름
3. app.py 생성<br>
- power-shell<br>
    new-item app.py<br>
- 내용<br>
    from flask import Flask<br>
    app = Flask(__name__)<br><br>
    
    @app.route('/')<br>
    def hello_world():<br>
        return 'Hello World!'<br><br>
    
    if __name__ == '__main__':<br>
        app.run()<br>
4.  flask 확인<br>
    python app.py<br>


----------
## 02. Virtualenv 설정
1. virtualenv 설정<br>
    pip install numpy<br>
    virtualenv venv<br>
    cd venv/Scripts<br>
    .\activate<br>
2. 필수 패키지 설치<br>
    pip install flask gunicorn jinja2<br>
3. Procfile 만들기 (Power-Shell)<br>
    new-item Procfile<br>
- 내용<br>
    web: gunicorn app:app<br>


----------
## 03. Requirements 만들기
1. 생성<br>
    pip freeze requirements<br>
    pip freeze > requirements.txt<br>
2. Encoding 방식 바꾸기<br>
  메모장으로 requirements.txt를 들어가서 `다른이름으로 저장하기`를 통해 ANSI로 저장함<br>


----------
## 04. Heroku에 Deploy
1. gitignore 생성 (Power-Shell)<br>
    new-item .gitignore<br>
2. git 시작하기<br>
    git init<br>
    git add --all<br>
    git commit -m "commit"<br>
3. heroku 접속<br>
    heroku login<br>
    heroku create<br>
    git remote -v<br>
    heroku  https://git.heroku.com/polar-tor-1665.git (fetch)<br>
    heroku  https://git.heroku.com/polar-tor-1665.git (push)<br>
    git push heroku master<br>
4. 연결 확인<br>

`https://polar-tor-1665.herokuapp.com/`<br>

5. 로그 태일<br>
    heroku logs --tail -a immense-springs-10641<br>
