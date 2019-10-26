from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from blogapp.models import *
import datetime
import json
import math
from django.utils import timezone
from django.core.files.storage import FileSystemStorage



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


# 判断是否是管理员身份
def is_admin(request):
    if request.session.get('is_boss') is True:
        return True
    else:
        return False


# 客户选择餐厅
def choose_name(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = Users.objects.get(username=username)
        if username is None:
            username = ' '
        canteen_num = str(request.POST.get('name'))
        # 拉取餐厅信息,拉取失败则返回选择页面
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_num': canteen_num,
            'warming': 1,
            'is_boss': 1 if user.is_boss else 0,
        }
        try:
            canteen = Canteen.objects.get(canteen_num=canteen_num)
            request.session['canteen_num'] = canteen_num
            return HttpResponseRedirect('/canteen/table/')
        except:
            return render(request, 'canteen/choose_name.html', txt)
    elif request.method == 'GET':
        # 观看博客者的username
        username = request.session.get('username')
        if username is None:
            username = ' '
        user = Users.objects.get(username=username)
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'is_boss': 1 if user.is_boss else 0,
        }
        return render(
            request,
            'canteen/choose_name.html',
            txt,
        )


# 客户选择餐桌
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


# 管理员新增餐桌
def add_table(request):
    is_admin(request)
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


# 选择用餐人数
def client_num(request, *args):
    # 餐桌号
    nums = args[0]
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    table = Table.objects.get(id=nums)
    table_num = table.table_num
    ls = [i + 1 for i in range(table_num)]
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
            'nums': nums,
            'ls': ls,
            'canteen_name': canteen.canteen_name,
        }
        return render(request, 'canteen/client_num.html', txt)
    else:
        clients = request.POST.get('client')
        print(type(clients), clients)
        table.table_clients = int(clients)
        table.is_over = False
        table.save()
        return HttpResponseRedirect(f'/canteen/p/{nums}/')


# 管理员新增菜单
def add_food(request):
    ret = is_admin(request)
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    username = request.session.get('username')
    if username is None:
        username = ' '
    if request.method == 'GET':
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_name': canteen.canteen_name,
        }
        if ret:
            return render(request, 'canteen/add_menu.html', txt)
        else:
            return  render(request, 'no_power.html')
    else:
        img = request.FILES.get('food_img')
        f2 = FileSystemStorage()
        path = f2.save('canteen/img/%s'%(img.name), img)   # 保存文件并返回文件名，如果文件名存在则会创建一个不重复的名称
        name = request.POST.get('food_name')
        price = request.POST.get('food_price')
        intro = request.POST.get('food_intro')
        num = request.POST.get('food_num')
        new_menu = Menu()
        new_menu.canteen = canteen
        new_menu.food_name = name
        new_menu.food_img = path
        new_menu.food_price = price
        new_menu.food_intro = intro
        new_menu.food_num = num
        new_menu.save()
        return HttpResponseRedirect('/canteen/table/')

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
        # client = dict_data['client_name']
        all_price = round(float(dict_data['all_price']), 2)
        length = int(dict_data['len'])
        for i in range(length):
            name = dict_data[f'foods[{i}][name]']
            nums = dict_data[f'foods[{i}][nums]']
            price = round(float(dict_data[f'foods[{i}][price]']), 2)
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


# 支付页面
def paying(request):
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    food_ls = request.session.get('food_ls')
    table = request.session.get('table')  # 桌号
    id = request.session.get('id')  # 消费记录id
    table_now = Table.objects.get(id=int(table))
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        history = ClientHistory.objects.get(id=id)
        paid = 1 if history.paid else 0
        is_over = 1 if table_now.is_over else 0
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
            'is_over': is_over,
        }
        return render(request, 'canteen/paying.html', txt)
    else:
        json_data = request.POST
        dict_data = eval(json.dumps(json_data, ensure_ascii=False))
        table_id = dict_data['table']
        if table == table_id:
            table_now.is_over = True
            table_now.table_clients = 0
            table_now.save()
            return HttpResponse(1)


# ajax检验是否支付成功
def check_paid(request):
    if request.method == 'POST':
        json_data = request.POST
        dict_data = eval(json.dumps(json_data, ensure_ascii=False))
        id = dict_data['id']
        history = ClientHistory.objects.get(id=id)
        paid = 1 if history.paid else 0
        return HttpResponse(paid)


# ajax支付
def wx_pay(request):
    if request.method == 'POST':
        id = request.session.get('id')
        history = ClientHistory.objects.get(id=id)
        history.paid = True
        history.save()
        return HttpResponse(1)


# 管理员页面,操作餐厅数据。
def adm_choose_canteen(request):
    ret = is_admin(request)
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        canteens = Canteen.objects.all()
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteens': canteens,
        }
        if ret:
            return render(request, 'canteen/admin_choose.html', txt)
        else:
            return render(request, 'no_power.html')

# 选择修改的内容
def adm_change_canteen(request, *args):
    ret = is_admin(request)
    canteen_id = args[0]
    request.session['change_canteen_id'] = canteen_id
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        canteen = Canteen.objects.get(id=canteen_id)
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen': canteen,
        }
        if ret:
            return render(request, 'canteen/admin_change.html', txt)
        else:
            return render(request, 'no_power.html')

# 修改餐厅名字
def adm_change_name(request):
    ret = is_admin(request)
    canteen_id = request.session.get('change_canteen_id')
    username = request.session.get('username')
    if username is None:
        username = ' '
    canteen = Canteen.objects.get(id=canteen_id)
    if request.method == 'GET':
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen': canteen,
        }
        if ret:
            return render(request, 'canteen/admin_change_name.html', txt)
        else:
            return render(request, 'no_power.html')
    else:
        new_name = request.POST.get('new_name')
        canteen.canteen_name = new_name
        canteen.save()
        return HttpResponseRedirect('/canteen/admin/change/'+canteen_id)


# 修改餐厅主管
def adm_change_boss(request):
    ret = is_admin(request)
    canteen_id = request.session.get('change_canteen_id')
    username = request.session.get('username')
    if username is None:
        username = ' '
    canteen = Canteen.objects.get(id=canteen_id)
    if request.method == 'GET':
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen': canteen,
        }
        if ret:
            return render(request, 'canteen/admin_change_boss.html', txt)
        else:
            return render(request, 'no_power.html')
    else:
        new_name = request.POST.get('new_name')
        canteen.canteen_boss = new_name
        canteen.save()
        return HttpResponseRedirect('/canteen/admin/change/'+canteen_id)


# 修改餐厅号
def adm_change_num(request):
    ret = is_admin(request)
    canteen_id = request.session.get('change_canteen_id')
    username = request.session.get('username')
    if username is None:
        username = ' '
    canteen = Canteen.objects.get(id=canteen_id)
    if request.method == 'GET':
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen': canteen,
        }
        if ret:
            return render(request, 'canteen/admin_change_num.html', txt)
        else:
            return render(request, 'no_power.html')
    else:
        new_num = request.POST.get('new_num')
        canteen.canteen_num = new_num
        canteen.save()
        return HttpResponseRedirect('/canteen/admin/change/'+canteen_id)


# 管理员查看历史订单
def adm_history(request):
    ret = is_admin(request)
    username = request.session.get('username')
    if username is None:
        username = ' '
    canteen_id = request.session.get('change_canteen_id')
    canteen = Canteen.objects.get(id=canteen_id)
    histories = ClientHistory.objects.filter(canteen_id=canteen.id)
    if request.method == 'GET':
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'canteen': canteen,
            'histories': histories,
            'username': username,
        }
        if ret:
            return render(request, 'canteen/admin_history.html', txt)
        else:
            return render(request, 'no_power.html')

