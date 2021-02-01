# import pymysql

# db = pymysql.connect(
#         user = 'root',
#         passwd = '',
#         host = '127.0.0.1',
#         port = 3306,
#         db = 'backend',
#         charset = 'utf8'
#     )

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    # g 객체에 db가 없다면?
    if 'db' not in g:
        # sqlite3를 불러옵니다.
        g.db = sqlite3.connect(
            # 현재 애플리케이션의 데이터베이스로 설정
            current_app.config['DATABASE'],
            # 반환되는 각 row에 대해 선언된 형을 구문분석
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # 튜플 형식이 아닌 접근하는 데이터를 dictionary 타입과 비슷하게 키-값 쌍으로 사용할 수 있게 해줌
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    # 글로벌 객체인 g에서 db를 추출
    db = g.pop('db', None)

    # db가 있다면 db를 종료
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # schema.sql의 파일을 열어 query를 실행
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# init-db 명령어를 shell에서 실행한다면 함수를 실행
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')
    

def init_app(app):
    # HTTP 요청이 완료되면 실행
    app.teardown_appcontext(close_db)
         # 새로운 shell 명령어를 추가
    app.cli.add_command(init_db_command)