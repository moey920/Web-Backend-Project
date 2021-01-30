import pymysql

db = pymysql.connect(
        user = 'root',
        passwd = '',
        host = '127.0.0.1',
        port = 3306,
        db = 'backend',
        charset = 'utf8'
    )
cursor = db.cursor(pymysql.cursors.DictCursor)

sql = "SELECT * FROM `boardarticle`"
cursor.execute(sql)
result = cursor.fetchall()
print(result)
# return jsonify(status = "success", result = result)