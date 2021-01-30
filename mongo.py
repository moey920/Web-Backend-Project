from flask import Flask
from flask_pymongo import PyMongo #1

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/WebBackendDB" #2
mongo = PyMongo(app) #3

board = mongo.db.board #4
test = { 
  "name": "test",
}
board.insert_one(test) #5

# 게시물 작성 시간 구하기
@app.template_filter("formatdatetime")
def format_datetime(value):
    if value is None:
        return ""

    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    value = datetime.fromtimestamp(int(value / 1000)) + offset  
    return value.strftime('%Y-%m-%d %H:%M:%S')

# html파일에서 jinja문법을 이용해 아래와 같이 위에서 작성한 필터 사용하여 DB에 저장된 작성시간 가공 가능
# {{result.pubdate|formatdatetime}}