import pymysql
from flask import Flask, jsonify, request, render_template, redirect, session, url_for, flash, g
from flask_restful import reqparse, abort, Api, Resource
from jinja2 import Template
import bcrypt
import re
import sql
import json


# User API 구현을 위한 새로운 패키지 로드
from flask import jsonify
from flask import request
from flask import session

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash


app = Flask(__name__)
api = Api(app) # flask에서 API 서버를 만들기 위해 플라스크 객체를 Api로 만듬

# DB 연결
db = pymysql.connect(
        user = 'root',
        passwd = '',
        host = '127.0.0.1',
        port = 3306,
        db = 'backend',
        charset = 'utf8'
    )
cursor = db.cursor()

# parser 변수를 통해 클라이언트로부터 전달 받는 인자들을 지정할 수 있다.
parser = reqparse.RequestParser()


"""
Board APIs - 게시판 CRUD

Create API : name 을 입력받아 새로운 게시판을 만듭니다.
Read API : 현재 등록된 게시판 목록을 가져옵니다.
Update API : 기존 게시판의 name 을 변경합니다.
Delete API : 특정 게시판을 제거합니다.
"""
# 게시판 APIs에서는 board 테이블의 id와 name만 인자로 받는다.
parser.add_argument('id')
parser.add_argument('name')

class Board(Resource): # Flask_restful 모듈의 Resource를 상속하여 기능을 모두 가지고 있다.(get 등)
    def get(self): # get 메소드로 http 요청을 보낼 때 아래의 함수가 실행된다.
        sql = "SELECT id, name FROM `board`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return jsonify(status = "success", result = result) # 전송여부를 확인하기 위해 status를 붙인다.
        
    def post(self):
        # 사용자가 입력한 값을 받아서 DB에 넣어야 한다. id는 Outoincrement이기 때문에 name(key)의 입력값(value)를 삽입한다.
        args = parser.parse_args()
        sql = "INSERT INTO `board` (`name`) VALUES (%s)"
        cursor.execute(sql, (args['name']))
        db.commit()
        
        return jsonify(status = "success", result = {"name": args["name"]})
        
    def put(self):
        args = parser.parse_args()
        sql = "UPDATE `board` SET name = %s WHERE `id` = %s"
        cursor.execute(sql, (args['name'], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"], "name": args["name"]})
    
    
    def delete(self):
        args = parser.parse_args()
        sql = "DELETE FROM `board` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})


"""
BoardArticle APIs - 게시판 글 CRUD

Create API : title, content 를 입력받아 특정 게시판(board)에 새로운 글을 작성합니다.
Read API : 게시판의 글 목록을 가져오거나, 특정 게시판(board)에 글의 내용을 가져옵니다.
Update API : 게시판 글의 title, content를 변경합니다.
Delete API : 특정 게시판 글을 제거합니다.
"""
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('content')
parser.add_argument('board_id')

class BoardArticle(Resource):
    def get(self, board_id=None, board_article_id=None):
        if board_article_id:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `id`=%s"
            cursor.execute(sql, (board_article_id,))
            result = cursor.fetchone()
        else:
            sql = "SELECT id, title, content FROM `boardArticle` WHERE `board_id`=%s"
            cursor.execute(sql, (board_id,))
            result = cursor.fetchall()
            
        return jsonify(status = "success", result = result)

    def post(self, board_id):
        args = parser.parse_args()
        sql = "INSERT INTO `boardArticle` (`title`, `content`, `board_id`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['title'], args['content'], args['board_id']))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"]})
        
        
    def put(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "UPDATE `boardArticle` SET title = %s, content = %s WHERE `id` = %s"
        cursor.execute(sql, (args['title'], args["content"], args["id"]))
        db.commit()
        
        return jsonify(status = "success", result = {"title": args["title"], "content": args["content"]})
        
        
    def delete(self, board_id=None, board_article_id=None):
        args = parser.parse_args()
        sql = "DELETE FROM `boardArticle` WHERE `id` = %s"
        cursor.execute(sql, (args["id"], ))
        db.commit()
        
        return jsonify(status = "success", result = {"id": args["id"]})

"""
User APIs : 유저 SignUp / Login / Logout

SignUp API : *fullname*, *email*, *password* 을 입력받아 새로운 유저를 가입시킵니다.
Login API : *email*, *password* 를 입력받아 특정 유저로 로그인합니다.
Logout API : 현재 로그인 된 유저를 로그아웃합니다.

user args : id, fullname, email, password
User API는 CRUD를 지키는 REST API 타입으로 생성할 필요는 없습니다.

따라서 이 실습에서는 CRUD를 다 지키지 않는 Login API를 구현합니다.
1번에 해당하는 “User APIs : 유저 SignUp / Login / Logout”를 직접 구현해보세요!
user 테이블 또한 직접 생생하셔야 합니다.
"""

# User APIs에서 사용한 args 들
parser.add_argument('id')
parser.add_argument('fullname')
parser.add_argument('email')
parser.add_argument('password')

# session을 위한 secret_key 설정
app.config.from_mapping(SECRET_KEY='dev')

@app.route('/')
def load_logged_in_user():
    # 현재 session에 등록된 유저의 정보 획득
    user_id = session.get('user_id')
    args = parser.parse_args()
    sql = "SELECT * FROM `user` WHERE `id`=%s"
    cursor.execute(sql, (id,))
    result = cursor.fetchone()
    
    return jsonify(status = "success", result = result)

@app.route('/register', methods=('GET', 'POST'))
def register():
    args = parser.parse_args()
    # POST 요청을 받았다면?
    if request.method == 'POST':
        # 아이디와 비밀번호를 폼에서 가져옵니다.
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        error = None
        
        # 아이디가 없다면?
        if not fullname:
            error = 'fullname이 유효하지 않습니다.'
        # email이 없다면?
        elif not email:
            error = 'email이 유효하지 않습니다.'
        # 비밀번호가 없다면?
        elif not password:
            error = 'Password가 유효하지 않습니다.'
        # 이름과 이메일과 비밀번호가 모두 있다면?
        else :
            sql = "SELECT * FROM `user` WHERE `id`=%s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone() 
            if result is not None:
                error = '{} 계정은 이미 등록된 계정입니다.'.format(email)

        # 에러가 발생하지 않았다면 회원가입 실행
        if error is None:
            args = parser.parse_args()
            sql = "INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (args['fullname'], args['email'], generate_password_hash(args['password'])))
            db.commit()
            return redirect(url_for('login'))
        # 에러 메세지를 화면에 나타냅니다. (flashing)
        flash(error)

    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    # POST 요청을 받았다면?
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        
        args = parser.parse_args()
        sql = "SELECT * FROM `user` WHERE `email` = %s"
        cursor.execute(sql, (args['email']))
        result = cursor.fetchone()
        
        # result = json.dumps(result)
        return jsonify(status = "success", result = result)
        # print(result)
        
        # 입력한 유저의 정보가 없을 때
        if result is None:
            error = '등록되지 않은 계정입니다.'
        elif not check_password_hash(result[3], password) :
            error = 'password가 틀렸습니다.'

        # 정상적인 정보를 요청받았다면?
        if error is None:
            # 로그인을 위해 기존 session을 비웁니다.
            session.clear()
            # 지금 로그인한 유저의 정보로 session을 등록합니다.
            session['user_id'] = result[0]
            return redirect(url_for('loggedin'))

        flash(error)

    return redirect(url_for('board'))


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect(url_for('index'))

"""
4. Dashboard APIs

RecentBoardArticle API : 모든 게시판에 대해 각각의 게시판의 가장 최근 *n* 개의 게시판 글의 *title* 을 가져옵니다. (*k* 개의 게시판이 있다면 최대 *k * n* 개의 게시판 글의 *title* 을 반환합니다.)
"""
class Dashboard(Resource):
    def get(self,dashboard_num):
        if dashboard_num:
            sql = "SELECT count(id) FROM board"
            cursor.execute(sql)
            count = cursor.fetchone()
            
            result = {}
            for i in range(1,count[0]+1):   
                sql = "SELECT title, boardArticle.create_date FROM  `boardArticle` WHERE board_id = %s ORDER BY boardArticle.create_date DESC LIMIT %s"
                cursor.execute(sql,(i, dashboard_num))
                result[i] = cursor.fetchall()

            return jsonify(status = "success", result= result)

# API Resource 라우팅을 등록! 이 api를 사용한다는 리소스를 보낸다. flask의 app.route()를 대신한다.
# 클래스가 하나의 API이고, resource(class)를 통해 class내의 메소드들을 모두 사용할 수 있다.
api.add_resource(Board, '/board')
api.add_resource(BoardArticle, '/board/<board_id>', '/board/<board_id>/<board_article_id>')
api.add_resource(Dashboard, '/dashboard/<int:dashboard_num>')


# if __name__ == '__main__' :
#     app.run('0.0.0.0', port=5000)
    
if __name__ == '__main__':
    app.run(debug=True)