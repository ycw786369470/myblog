from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import datetime
from django.utils import timezone
from blogapp.models import *
import math
from datetime import timedelta
from django.db.models import F,Q
from django.views.generic import ListView
import re
import hashlib


now_time = datetime.date.today()
this_week = now_time.isoweekday()
all_blogs = BlogUser.objects.all()
all_user = Users.objects.all()
all_comment = Comment.objects.all()
new_blogs = all_blogs[0:5]
comment = all_comment[0:5]


# 以上为默认上传的两边内容
# Create your views here.
def about(request):
    username = request.session.get('username')
    if username == None:
        username = ' '
    txt = {
        'users': all_user,
        'now_time': now_time,
        'this_week': this_week,
        'comment': comment,
        'new_blog': new_blogs,
        'username': username,
    }
    return render(request, 'blog/about.html', txt)


def content(request):
    return render(request, 'blog/content.html')


def person(request):
    if request.method == 'GET':
        username = request.session.get('username')
        if username is None:
            username = ' '
        # 个人内容
        self = Users.objects.get(username=username)
        gender = '男' if self.gender == True else '女'
        up_num = UserUp.objects.filter(mark_name=self)
        star_num = UserStar.objects.filter(mark_name=self)
        txt = {
            'now_time': now_time,
            'this_week': this_week,
            'comment': comment,
            'new_blog': new_blogs,
            'username': username,
            'self': self,
            'gender': gender,
            'up': up_num.count(),
            'star': star_num.count(),
        }
        return render(request, 'blog/person.html', txt)


def message(request):
    # 观看博客者的username
    username = request.session.get('username')
    if username is None:
        username = ' '
    all_msg = Message.objects.all()[0: 5]
    if request.method == 'POST':
        name = request.POST.get('commentName')
        email = request.POST.get('commentEmail')
        comment = request.POST.get('commentContent')
        msg = Message()
        msg.name = name
        msg.time = timezone.now()
        msg.email = email
        msg.content = comment
        msg.save()
        print(f'{username}发表评论')

    txt = {
        'users': all_user,
        'now_time': now_time,
        'this_week': this_week,
        'comment': comment,
        'new_blog': new_blogs,
        'username': username,
        'message': all_msg,
    }
    return render(request, 'blog/message.html', txt)


def index(request, *args):
    now_time = datetime.date.today()
    this_week = now_time.isoweekday()
    # 博客主页
    num = int(args[0])
    content_num = 5     # 每页条数
    page_back, page_next = num - 1, num + 1
    all_blogs = BlogUser.objects.all()
    page = len(all_blogs)
    page_num = int(math.ceil(page/content_num))
    page_ls = [i for i in range(1, page_num + 1)]
    new_blogs = all_blogs[0:5]
    blogs = all_blogs[(num - 1) * content_num: num * content_num]
    # 热门评论
    comment = Comment.objects.all()[0:5]
    # 本周热门,获取本周第一天和最后一天
    start_day = now_time - timedelta(this_week - 1)
    end_day = now_time + timedelta(7 - this_week)
    week_hot = all_blogs.filter(Q(time__gt=start_day) | Q(time__lt=end_day))[0:4]
    # 广告位
    friend_link = FriendLink.objects.all()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username)
            if user.password == password:
                request.session['username'] = username
                return HttpResponseRedirect('/blog/index/1')
        except:
            warming_msg = '账号或密码错误！'
            return render(request, 'blogapp/login.html', {'username': username,
                                                          'warming': warming_msg})
    else:
        try:
            username = request.session.get('username')
        except:
            username = ' '
        txt = {
            'now_time': now_time,
            'this_week': this_week,
            'blogs': blogs,
            'page': num,
            'pageback': page_back,
            'pagenext': page_next,
            'page_ls': page_ls,
            'comment': comment,
            'new_blog': new_blogs,
            'week_hot': week_hot,
            'friend_link': friend_link,
            'username': username,
        }
        return render(request, 'blog/index.html', txt)


def detail(request, *args):
    # 观看博客者的username
    username = request.session.get('username')
    if username == None:
        username = ' '
    mark_user = Users.objects.get(username=username)
    # 获取当前时间
    num = args[0]
    blog = BlogUser.objects.get(id=num)
    blog.visit += 1
    blog.save()
    # 上一篇/下一篇
    previous_blog = all_blogs.filter(id__lt=num).order_by('-id')[:1]
    next_blog = all_blogs.filter(id__gt=num)[:1]
    pre_blog = all_blogs.get(id=num)    # 当前博客
    # 评论
    pre_comment = all_comment.filter(user_id=num)
    # 相关推荐
    same_tag_blogs = all_blogs.filter(tag=pre_blog.tag)
    # 赞、踩
    try:
        marks = Mark.objects.get(name_id=num)
    except Exception as e:
        new_mark = Mark()
        new_mark.mark_name_id = mark_user.id
        new_mark.name_id = blog.id
        new_mark.save()
        print('当前文章无点赞实例,新建实例成功！')
    try:
        # 尝试获取UserUp的外键BlogUser即name, 若抛出错误则表示没有该用户数据
        # 则需添加该用户对博主mark的数据
        mark_up = UserUp.objects.filter(mark_name=mark_user)
        # 确认可以取到关联mark者和文章的关系，取不到任然会抛出错误
        up = mark_up.get(name=blog)
        # print('取到了不要添加！')
    except:
        new_up = UserUp()
        new_up.name = blog
        new_up.mark_name = mark_user
        new_up.save()
        new_down = UserDown()
        new_down.name = blog
        new_down.mark_name = mark_user
        new_down.save()
        new_star = UserStar()
        new_star.name = blog
        new_star.mark_name = mark_user
        new_star.save()
        print('添加mark数据成功！')
    marks = Mark.objects.get(name_id=num)
    # 添加评论
    if request.method == 'POST':
        new_com = request.POST.get('commentContent')
        com = Comment()
        com.name = mark_user
        com.time = timezone.now()
        com.user = blog
        com.content = new_com
        com.save()

    txt = {
        'now_time': now_time,
        'this_week': this_week,
        'comment': comment,
        'new_blog': new_blogs,
        'pre_blog': pre_blog,
        'previous_blog': previous_blog,
        'next_blog': next_blog,
        'pre_comment': pre_comment,
        'same_tag_blogs': same_tag_blogs,
        'username': username,
        'mark': marks,
        'num': num,
    }
    return render(request, 'blog/detail.html', txt)


def calc(request):
    # 取得当前博客的点击信息(赞，踩，还是收藏)
    num = request.POST.get('num')
    mark_method = request.POST.get('mark')
    mark_name = request.POST.get('mark_name')
    # 查找mark的user
    name = request.POST.get('blog_name')
    mark_user = Users.objects.get(username=mark_name)
    # 博主的Users对象
    # user = Users.objects.get(username=name)
    # 先根据名字获取对应的BlogUser
    user = BlogUser.objects.get(id=num)
    # 反向查询
    mark = Mark.objects.filter(name_id=user)[0]
    # 获取需要加上mark数量的元素
    mark_num = 0
    # 判断点击的是赞、踩还是收藏,并分别取出+1再存入
    if mark_method == 'up':
        print(f'{mark_name}正在给{name}的文章点赞！')
        # 判断是否点赞过此文章
        # 过滤出当前文章对应的数据
        print(user.id)
        print(mark_user.id)
        mark_up = UserUp.objects.filter(name=user).filter(mark_name=mark_user)[0]
        print(mark_up.is_over)
        if mark_up.is_over is False:
            # 该用户已经点过赞
            mark_up.is_over = True
            mark_up.save()
            mark_num = mark.up_num + 1
            mark.up_num = mark_num
        else:
            print('但是已经点过啦')
            mark_num = mark.up_num
    elif mark_method == 'down':
        mark_down = UserDown.objects.filter(name=user).filter(mark_name=mark_user)[0]
        if mark_down.is_over is False:
            mark_down.is_over = True
            mark_down.save()
            mark_num = mark.down_num + 1
            mark.down_num = mark_num
        else:
            mark_num = mark.down_num
    mark.save()
    # 给ajax返回success
    return HttpResponse(mark_num)


def login(request):
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
        }
        return render(request, 'blog/login.html', txt)
    else:
        username = request.session.get('username')
        if username is None:
            username = ' '
        username_input = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username_input)
            # 登陆成功
            md5_psw = hashlib.md5()
            md5_psw.update(password.encode(encoding='utf-8'))
            if user.password == md5_psw.hexdigest():
                request.session['username'] = username_input
                if user.is_boss:
                    request.session['is_boss'] = True
                else:
                    request.session['is_boss'] = False
                return HttpResponseRedirect('/blog/index/1/')
            # 密码不对应
            else:
                warming = '密码错误！'
                txt = {
                    'username': username,
                    'username_input': username_input,
                    'warming': warming,
                    'users': all_user,
                    'now_time': now_time,
                    'this_week': this_week,
                    'comment': comment,
                    'new_blog': new_blogs,
                }
                return render(request, 'blog/login.html', txt)
        except:
            warming = '账号不存在！'
            txt = {
                'warming': warming,
                'username': username,
                'users': all_user,
                'now_time': now_time,
                'this_week': this_week,
                'comment': comment,
                'new_blog': new_blogs,
            }
            return render(request, 'blog/login.html', txt)


def register(request):
    if request.method == 'GET':
        username = request.session.get('username')
        if username == None:
            username = ' '
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
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
        return render(request, 'blog/register.html', txt)
    elif request.method == 'POST':
        tooshort_warming = '密码长度不符！请重新输入'
        password_warming = '两次密码不匹配！请重新输入'
        username_warming = '账号已存在！请重新输入'
        all_num_warming = '账号或密码不能为纯数字！'
        # 分别取得昵称 账号 密码 确认密码 性别 爱好
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        gender = request.POST.get('gender')
        habits = request.POST.get('habits')
        reg_html = 'blog/register.html'
        # 判断账号是否是纯数字
        if username.isdigit() == True and password.isdigit() == True:
            return render(request, reg_html, {'name': name,
                                                             'warming': all_num_warming})
        # 判断密码是否过短或过长,正则判断法
        if not re.match('[0-9a-zA-Z!@#$%^&*]{8,16}', password):
            return render(request, reg_html, {'name': name,
                                                             'warming': tooshort_warming})
        # 确认两次密码相同
        if password == password2:
            # 确认账号没有重复
            users = Users.objects.filter(username=username)
            if len(users) == 0:
                # 判断可以新建账号后添加至数据库
                new_user = Users()
                new_user.photo = 'blog/default_photo.png'
                new_user.name = name
                new_user.username = username
                # new_user.password = password
                # hash md5加密型密码
                hash_md5 = hashlib.md5()
                hash_md5.update(password.encode(encoding='utf-8'))
                md5_psw = hash_md5.hexdigest()
                new_user.password = md5_psw
                # 性别
                new_gender = True if gender == '1' else False
                new_user.gender = new_gender
                new_user.habits = Tag.objects.get(id=habits)
                new_user.save()
                request.session['username'] = username
                print('新增账号成功！')
                return HttpResponseRedirect('/blog/index/1/')
            # 账号重复，重新填写账号
            else:
                return render(request, reg_html, {'name': name,
                                                    'warming': username_warming})
        else:
            return render(request, reg_html, {'name': name,
                                                'warming': password_warming})


def addblog(request):
    username = request.session.get('username')
    if username == None:
        username = ' '
    if request.method == 'GET':
        now_time = datetime.date.today()
        this_week = now_time.isoweekday()
        all_blogs = BlogUser.objects.all()
        all_user = Users.objects.all()
        all_comment = Comment.objects.all()
        new_blogs = all_blogs[0:5]
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
        return render(request, 'blog/addblog.html', txt)
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = str(request.POST.get('content'))
        tag = request.POST.get('tag')
        user = Users.objects.get(username=username)
        blog = BlogUser()
        blog.name = user
        blog.title = title
        blog.content = content
        blog.time = timezone.now()
        blog.tag = Tag.objects.get(id=tag)
        blog.save()
        print('添加完成')
        return HttpResponseRedirect('/blog/index/1/')