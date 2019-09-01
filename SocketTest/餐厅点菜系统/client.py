    # 点菜系统客户端
# 基于TCP连接
# 1-进入系统选座
# 2-选择登录、注册、点菜
# 3-根据选择数字操作

import redis
from socket import *
from . import sql
import json

# 建立套接字
def make_socket():
    s = socket(AF_INET, SOCK_STREAM)
    ip_port = ('192.168.1.122',6666)
    s.connect(ip_port)
    print('连接服务端成功')
    return s

# 登录
def login(s):
    print('======================登录========================')
    username = input('请输入您的账号>>>')
    password = input('请输入您的密码>>>')
    log_dict = {'func': 'login',
                'data':{
                    'username': username,
                    'password': password
                }
    }
    log_dict = json.dumps(log_dict).encode('gbk')
    s.send(log_dict)
    return username

# 注册
def register(s):
    print('======================注册界面========================')
    username = input('请设置您的账号>>>')
    password = input('请设置您的密码>>>')
    log_dict = {'func': 'register',
                'data':{
                    'username': username,
                    'password': password
                }
    }
    log_dict = json.dumps(log_dict).encode('gbk')
    s.send(log_dict)
    return username

# 选择界面
def choose():
    print('请输入数字选择以下选项——1、登录 2、注册 3、点菜')
    choose_num = eval(input('>>>'))
    if choose_num not in [0, 1, 2, 3, 4]:
        print('输入错误，请重新输入')
        choose()
    return choose_num

# 展示菜单以及点菜
def menu(s, c, name, table):
    # 通过数据库获取菜单
    menu = sql.get_menu(c)
    print('###########################菜单##########################')
    for i in menu:
        print('Num:{:}\tFoodName:{:}\t\t\tPrice:${:}'.format(i[0], i[1], i[2]))
    print('#########################################################')
    print('请输入您点菜的序号(直接回车结束点菜)')
    food_nums = []              # 存放点菜数据
    money = 0                   # 计算总价
    while True:
        food = input('>>>')
        if len(food) == 0:
            break
        food = int(food)
        food_nums.append(food)
        money += menu[food - 1][2]  # 计算价格
        print('已点${:}'.format(money))

    sattle(s, money, name, table, food_nums)

# 结账
def sattle(s, money, name, table, food_nums):
    print('您消费的总价为:${:}。是否立即支付?'.format(money))
    sat = {'func': 'sattle',
           'data':{
                'food': food_nums,
                'table': table,
                'username': name,
                'price': money
           }
       }
    sat = json.dumps(sat).encode('gbk')
    s.send(sat)
    print('等待服务端确认...')

# def recv():
#     global s
#     recv_data = s.recv(1024).decode('gbk')
#     print(recv_data)

def main():
    c, db = sql.log_sql('cantee')
    # 创建套接字
    s = make_socket()
    username = 'null'

    # t = threading.Thread(target=recv)
    # t.start()
    ####################主流程################
    # 1、选择桌号
    print('请输入您的桌号')
    table_num = eval(input('>>>'))

    # 2、选择界面
    while 1:
        choose_num = choose()
        # 登录
        if choose_num == 1:
            username = login(s)
        # 注册
        elif choose_num == 2:
            username = register(s)
        # 点菜
        elif choose_num == 3:
            menu(s, c, username, table_num)
            break
        # 结账功能在点菜中实现
    s.close()



if __name__ == '__main__':
    main()

