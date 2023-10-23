import pymysql

db = pymysql.connect(host="localhost", user="root", password="wwzzxx123", database="chatglm_webserver", charset="utf8")
cursor = db.cursor()
userid = "user1"
password = "123456"
sql =  "insert into accounts(id, password) values (' " + userid + " ', ' " + password + " ')"
cursor.execute(sql)

sql = "select * from accounts where id=" + userid + " and password=" + password
cursor.execute(sql)
results = cursor.fetchall()
print(results)
db.commit()
db.close()