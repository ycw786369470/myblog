# 点菜系统服务端
# 基于TCP连接

from socket import *
from . import sql
import json
import select


def make_socket():
    s = socket(AF_INET, SOCK_STREAM)
    ip_port = ('192.168.1.122', 6666)
    s.bind(ip_port)
    s.listen(10)
    return s

# 去数据库中注册
def register(c, username, password):
    sql.create_user(c, username, password)
    print('新用户注册成功！')

def login(c, username, password):
    ret = sql.ensure_user(c, username, password)
    if password == ret[0]:
        print('登录成功！')
    else:
        print('登录失败')

def get_food_name(c, food_ls):
    menu = sql.get_menu(c)
    foods = []
    money = 0
    for i in food_ls:
        d = {'name':menu[i - 1][1], 'price':menu[i - 1][2]}
        foods.append(d)
        money += menu[i - 1][2]
    return foods, money

def main():
    # 连接数据库
    c, db = sql.log_sql('cantee')
    # 创建套接字
    s = make_socket()
    # 监听列表
    listen = [s]
    print('点餐服务器已打开')
    while 1:
        rlist, wlist, elist = select.select(listen, [], [], 1) # rlist为就绪的元素
        for con in rlist:
            # 有新用户连接进来
            if con == s:
                client,addr = s.accept()
                client_ip = addr[0] #新用户的ip
                client_port = addr[1] #新用户的端口号
                print('有新用户加入！IP地址为:', client_ip, '端口号为', client_port)
                listen.append(client)
            # 已连接的用户发来信息
            else:
                data = con.recv(1024).decode('gbk')
                # 过滤掉无用信息
                if len(data) == 0:
                    continue
                else:
                    # data是字典形式的
                    data = eval(data)
                    # 取得传送过来的是哪种内容：注册register/登录login/结账sattle
                    func = data.get('func')
                    if func == 'register':
                        username = data['data']['username']
                        password = data['data']['password']
                        register(c, username, password)
                    elif func == 'login':
                        username = data['data']['username']
                        password = data['data']['password']
                        login(c, username, password)
                    elif func == 'sattle':
                        data = data['data']
                        food_ls = data.get('food')
                        table_num = data.get('table')
                        username = data.get('username')
                        price = data.get('price')
                        # 去链接数据库取得菜名以及价格
                        food,money = get_food_name(c, food_ls)
                        # 确认价格
                        if price == money:
                            con.send('已接单！'.encode('gbk'))
                            print('{:}号桌接单成功！\t用户{:}点的菜有：'.format(table_num, username))
                            for f in food:
                                print('{:}——{:}'.format(f.get('name'),f.get('price')))




if __name__ == '__main__':
    main()
