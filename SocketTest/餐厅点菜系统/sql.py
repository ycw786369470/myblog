import pymysql

def log_sql(sql_name,root = 'root',password = '123'): #连接数据库
    db = pymysql.connect('localhost', root, password, sql_name)
    print('连接数据库成功')
    cursor = db.cursor() #获取一个游标
    return cursor,db # 返回游标和db

def create_user(c, username, password):
    sql = 'insert into users(username,password) values("{:}","{:}")'.format(username, password)
    c.execute(sql)

def ensure_user(c, username, password):
    sql = 'select password from users where username = "{:}";'.format(username)
    c.execute(sql)
    data = c.fetchall()[0]
    return data


def get_menu(c):
    sql = 'select * from menu;'
    c.execute(sql)
    data = c.fetchall()
    return data

