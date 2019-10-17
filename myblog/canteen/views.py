from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from blogapp.models import *
import datetime


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
        # 获取当前时间
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
        # 热门评论
        comment = all_comment[0:5]
        # 以上为默认上传的两边内容
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
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
        comment = all_comment[0:5]
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
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
        comment = all_comment[0:5]

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


# 点菜
def menu(request, *args):
    num = args[0]
    canteen_num = request.session.get('canteen_num')
    canteen = Canteen.objects.get(canteen_num=canteen_num)
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
        comment = all_comment[0:5]

        menu = Menu.objects.filter(canteen=canteen)
        txt = {
            'users': all_user,
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'canteen_name': canteen.canteen_name,
            'menu': menu,
        }
        return render(request, 'canteen/menu.html', txt)
    else:
        pass
