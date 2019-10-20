from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from blogapp.models import *
import datetime
import json
import math
from django.utils import timezone


# 两边内容
# 获取当前时间
now_time = datetime.date.today()
this_week = now_time.isoweekday()
all_blogs = BlogUser.objects.all().order_by('-time')
all_user = Users.objects.all()
all_comment = Comment.objects.all().order_by('-time')
new_blogs = all_blogs[0: 5]
# 热门评论
comment = all_comment[0: 5]


# 以上为默认上传的两边内容


# Create your views here.
def choose_name(request):
    if request.method == 'POST':
        canteen_num = str(request.POST.get('name'))
        # 拉取餐厅信息,拉取失败则返回选择页面
        try:
            canteen = Canteen.objects.get(canteen_num=canteen_num)
            request.session['canteen_num'] = canteen_num
            return HttpResponseRedirect('/canteen/table/')
        except:
            return render(request, 'canteen/choose_name.html', {'canteen_num': canteen_num,
                                                                'warming': 1,
                                                                })
    elif request.method == 'GET':
        # 观看博客者的username
        username = request.session.get('username')
        if username is None:
            username = ' '

        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
        }
        return render(
            request,
            'canteen/choose_name.html',
            txt,
        )


def choose_table(request):
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '

        user = Users.objects.get(username=username)
        tables = Table.objects.filter(canteen=canteen)
        txt = {
            'table_nums': tables,
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'is_boss': 1 if user.is_boss else 0,
            'canteen_name': canteen.canteen_name,
        }
        return render(request, 'canteen/choose_table.html', txt)


def add_table(request):
    # 获取店名
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '

        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_name': canteen.canteen_name,
        }
        return render(request, 'canteen/add_tables.html', txt)
    else:
        max_chars = request.POST.get('max_chars')
        new_table = Table()
        new_table.canteen = canteen
        new_table.table_num = max_chars
        new_table.is_over = True
        new_table.save()
        print('添加桌位成功！')
        return HttpResponseRedirect('/canteen/table/')


def add_food(request):
    if request.method == 'GET':
        pass
    else:
        pass


# 点菜
def menu(request, *args):
    # 餐桌号
    num = args[0]
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    username = request.session.get('username')
    if username is None:
        username = ' '
    if request.method == 'GET':
        canteen_menu = Menu.objects.filter(canteen=canteen)
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_name': canteen.canteen_name,
            'menu': canteen_menu,
            'table_num': num,
        }
        return render(request, 'canteen/menu.html', txt)
    else:
        user = Users.objects.get(username=username)
        json_data = request.POST
        # 将json文件转化成字典文件
        dict_data = eval(json.dumps(json_data, ensure_ascii=False))
        # 提取数据给厨房（boss）查看
        food_ls = []
        # 保存至数据库的菜单
        food_data = []
        table = dict_data['table_num']
        client = dict_data['client_name']
        all_price = round(float(dict_data['all_price']), 2)
        length = int(dict_data['len'])
        for i in range(length):
            name = dict_data[f'foods[{i}][name]']
            nums = dict_data[f'foods[{i}][nums]']
            price = dict_data[f'foods[{i}][price]']
            if int(nums) > 0:
                d = {
                    'Name': name,
                    'Nums': nums,
                    'Price': price,
                }
                food_ls.append(d)
                food_data.append(f'【{name}】*{nums}')
        request.session.set_expiry(0)   # 关闭浏览器则清空session
        food_data = '——'.join(food_data)
        # 保存数据
        c_history = ClientHistory()
        c_history.client = user
        c_history.canteen = canteen
        c_history.consume_time = timezone.now()
        c_history.food = food_data
        c_history.price = all_price
        c_history.table = int(table)
        c_history.save()
        request.session['food_ls'] = food_ls
        request.session['table'] = table
        request.session['id'] = c_history.id
        return HttpResponse('/canteen/paying/')


# 支付
def paying(request):
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        food_ls = request.session.get('food_ls')
        table = request.session.get('table')
        id = request.session.get('id')
        history = ClientHistory.objects.get(id=id)
        paid = 1 if history.paid else 0
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_name': canteen.canteen_name,
            'food_ls': food_ls,
            'table': table,
            'id': id,
            'paid': paid,
        }
        return render(request, 'canteen/paying.html', txt)


# ajax检验是否支付成功
def check_paid(request):
    if request.method == 'POST':
        json_data = request.POST
        dict_data = eval(json.dumps(json_data, ensure_ascii=False))
        id = dict_data['id']
        history = ClientHistory.objects.get(id=id)
        paid = 1 if history.paid else 0
        return HttpResponse(paid)

