'''
    主页:
        通过bootstrap框架作为搭建练习，没啥luan用，可通过“博客”超链接进入博客主界面
    本地urls（局域网地访问地址会改变）：
        1、主页        127.0.0.1:8000/main/
        2、博客        127.0.0.1:8000/main/blog/1/
        3、登录        127.0.0.1:8000/main/login/
        4、注册        127.0.0.1:8000/main/register/
        5、添加博客    127.0.0.1:8000/main/addblog/
        6、个人中心    127.0.0.1:8000/main/person/
        ...
    目前用户功能:
        1、登录
            必要属性：①用户名
                      ②密码
        2、注册
            必要属性：①用户名（暂时不限最低字数，由中文或数字、符号组成）
                      ②密码（不低于8位，由字母、数字、符号组成）
                      ③需再次确认密码
                      ④用户头像为默认头像，可以注册后在个人中心上传
                      ⑤昵称可以自定义，可以为中文
        2、发表博客文章（必须登录，游客禁止）
            必要属性：①标题——title    ②内容——content    ③标签——tag     ④登录用户信息
            防止出bug暂时不用富文本
        3、查看文章详情对文章评论（登录后评论名为自己id，不登录评论名则为游客）
            必要属性：①评论内容      ②用户登录信息
        4、用ajax对文章赞、踩、收藏（必须登录，游客禁止）
            必要属性：①登录信息     ②每个账户对一篇文章只能赞、踩、收藏一次！
        5、个人中心（登陆后才能访问）
            修改个人信息以及查看点赞、踩、收藏过的文章
    博客页面功能：
        1、分页功能，每页五条文章，有上一页、下一页、回到首页等翻页功能
        2、如果某一页没有内容，则会调用{% empty %}内容
'''


from DjangoUeditor.models import UEditorField
from django.core.mail import send_mail, send_mass_mail
# from ..myblog import settings
from django.shortcuts import render
from .models import *
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
import re
import hashlib      # 加密
from django.views.decorators.cache import cache_page    # 导入视图缓存SDADAWDRFC


# 重定向简写函数
from django.shortcuts import redirect


# 假如访问127.0.0.1则自动跳转到127.0.0.1/main/页面
def redict_test(request):
    pass


# Create your views here.
def req_info(request):
    return HttpResponse(
        '请求方法{},请求url{}，编码格式{}'.format(request.scheme,
                                                  request.path,
                                                  request.body))


# @cache_page(60*15)
def get_info(request):
    a = request.GET.get('a')
    b = request.GET.get('b')
    c = request.GET.get('c')
    dict = {
        'a': a,
        'b': b,
        'c': c
    }
    return JsonResponse(dict)


def main(request):
    return render(request, 'blogapp/main.html')


# 接收num当前页数
def blog(request, num):
    # 每页博客条数
    content_num = 5
    num = int(num[0])
    page_back, page_next = num - 1, num + 1
    blogs = BlogUser.objects.all()[(num - 1) * content_num: num * content_num]
    if request.method == 'GET':
        username = request.session.get('username')
        print(username, '正在访问博客主页')
        return render(request, 'blogapp/blog.html', {'blogs': blogs,
                                                     'page': num,
                                                     'pageback': page_back,
                                                     'pagenext': page_next,
                                                     'name': username})
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = Users.objects.get(username=username)
            if user.password == password:
                request.session['username'] = username
                # return render(request, 'blogapp/blog.html', {'blogs': blogs,
                #                                              'page': num,
                #                                              'pageback': page_back,
                #                                              'pagenext': page_next,
                #                                              'name': username,
                #                                              'username': username})
                return HttpResponseRedirect('/blog/index/1/')
        except:
            warming_msg = '账号或密码错误！'
            return render(request, 'blogapp/login.html', {'username': username,
                                                          'warming': warming_msg})


def comment(request, *args):
    # 文章id
    id = args[0]
    # 浏览文章的用户名，不是作者用户名
    username = request.session.get('username')
    if username is None:
        username = ' '
        print(username, '访问文章：', id)
    # 获取mark用户的Users内容
    mark_user = Users.objects.get(username=username)
    # 根据id获取该篇文章BlogUser
    blog = BlogUser.objects.get(id=id)

    # 发表评论
    if request.method == 'POST':
        new_com = request.POST.get('com_text')
        com = Comment()
        com.name = mark_user
        com.time = timezone.now()
        com.user = blog
        com.content = new_com
        com.save()

    # 尝试获取UserUp的外键BlogUser即name, 若抛出错误则表示没有该用户数据
    # 则需添加该用户对博主mark的数据
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

    # 获取marks
    # 如果mark为空则说明之前没有该作者的评论,则新建一条对应的默认数为0
    try:
        marks = Mark.objects.get(name_id=id)
    except:
        new_mark = Mark()
        new_mark.mark_name_id = mark_user.id
        new_mark.name_id = blog.id
        new_mark.save()
        print('当前文章无点赞实例,新建实例成功！')
    # 再次获取mark数据信息
    marks = Mark.objects.get(name_id=id)
    # 查询对该博主文章的评论
    all_comment = Comment.objects.all()
    comments = []
    for c in all_comment:
        if c.user_id == int(id):
            comments.append(c)
        else:
            continue
    return render(request, 'blogapp/blog_detail.html', {
        'blog': blog,
        'comment': comments,
        'mark': marks,
        'name': username,
    })


def calc(request):
    dict_data = eval(str(request.POST)[12:-1])
    # 取得当前博客的点击信息(赞，踩，还是收藏)
    mark_method = dict_data['mark'][0]
    name = dict_data['blog_name'][0]
    # 查找mark的user
    # mark_name = dict_data['mark_name'][0]
    mark_name = request.session.get('username')
    mark_user = Users.objects.get(username=mark_name)
    # 博主的Users对象
    user = Users.objects.get(name=name)
    # 先根据名字获取对应的BlogUser
    user = BlogUser.objects.filter(name=user)[0]
    # 反向查询
    mark = Mark.objects.filter(name_id=user)[0]
    # 获取需要加上mark数量的元素
    mark_num = 0
    # 判断点击的是赞、踩还是收藏,并分别取出+1再存入
    if mark_method == 'up':
        print(f'{mark_name}正在给{name}的文章点赞！')
        # 判断是否点赞过此文章
        # 过滤出当前文章对应的数据
        mark_up = UserUp.objects.filter(name=user).filter(mark_name=mark_user)[0]
        if mark_up.is_over == False:
            # 该用户已经点过赞
            mark_up.is_over = True
            mark_up.save()
            mark_num = mark.up_num + 1
            mark.up_num = mark_num
        else:
            mark_num = mark.up_num
    elif mark_method == 'down':
        mark_down = UserDown.objects.filter(name=user).filter(mark_name=mark_user)[0]
        if mark_down.is_over == False:
            mark_down.is_over = True
            mark_down.save()
            mark_num = mark.down_num + 1
            mark.down_num = mark_num
        else:
            mark_num = mark.down_num
    elif mark_method == 'star':
        mark_star = UserStar.objects.filter(name=user).filter(mark_name=mark_user)[0]
        if mark_star.is_over == False:
            mark_star.is_over = True
            mark_star.save()
            mark_num = mark.star_num + 1
            mark.star_num = mark_num
        else:
            mark_num = mark.star_num
    mark.save()
    # 给ajax返回success
    return HttpResponse(mark_num)


def add_blog(request, *args):
    username = request.session.get('username')
    if request.method == 'POST':
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
        return HttpResponseRedirect('/main/blog/1')
    elif request.method == 'GET':
        form = DjangoForm()
        txt = {
            'name': username,
            'form': form,
        }
        return render(request, 'blogapp/add_blog.html', txt)


def add_blog_ok(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = str(request.POST.get('content'))
        tag = request.POST.get('tag')
        blog = BlogUser()
        blog.name = title
        blog.content = content
        blog.time = timezone.now()
        blog.tag = Tag.objects.get(id=tag)
        blog.save()
        print('添加完成')
        return render(request, 'blogapp/add_blog_ok.html')
    else:
        return HttpResponse('404--ERROR')


# 登录界面
def login(request):
    return render(request, 'blogapp/login.html')


def register(request):
    return render(request, 'blogapp/register.html')


def registering(request):
    if request.method == 'POST':
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

        # 判断账号是否是纯数字
        if username.isdigit() == True and password.isdigit() == True:
            return render(request, 'blogapp/register.html', {'name': name,
                                                             'warming': all_num_warming})
        # 判断密码是否过短或过长
        # if 8 < len(password) < 16:
        # 正则判断法
        if not re.match('[0-9a-zA-Z!@#$%^&*]{8,16}', password):
            return render(request, 'blogapp/register.html', {'name': name,
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
                new_user.password = password
                # 加密型密码
                # s = hashlib.sha1()
                # s.update(password.encode('utf-8'))
                # password = s.hexdigest()
                new_gender = True if gender == '1' else False
                new_user.gender = new_gender
                new_user.habits = Tag.objects.get(id=habits)
                new_user.save()
                request.session['username'] = username
                print('新增账号成功！')
                return render(request, 'blogapp/registering.html')
            # 账号重复，重新填写账号
            else:
                return render(request, 'blogapp/register.html', {'name': name,
                                                                 'warming': username_warming})
        else:
            return render(request, 'blogapp/register.html', {'name': name,
                                                             'warming': password_warming})


def person(request, *args):
    if request.method == 'GET':
        username = request.session.get('username')
        user = Users.objects.get(username=username)
        up_index = 0
        down_index = 0
        star_index = 0
        up_num = UserUp.objects.filter(mark_name=user)
        down_num = UserDown.objects.filter(mark_name=user)
        star_num = UserStar.objects.filter(mark_name=user)
        for up in up_num:
            if up.is_over is True:
                up_index += 1
        for down in down_num:
            if down.is_over is True:
                down_index += 1
        for star in star_num:
            if star.is_over is True:
                star_index += 1
        return render(request, 'blogapp/person.html', {
            'user': user,
            'up_index': up_index,
            'down_index': down_index,
            'star_index': star_index,
        })


def base(request):
    return render(request, 'blogapp/base.html')


# def send_mass_msg(request):
#     msg = ('邮件标题',
#            '<a href="#">haha</a>',
#            settings.EMAIL_FROM,
#            ['786369470@qq.com']
#            )
#     send_mass_mail(msg)


def send_msg(request):
    '''
        邮件参数
        subject: 邮件主题
        message: 邮件文本内容
        from_email: 发送者邮箱
        recipient: 接受者邮箱， 支持群发
        fail_silently : 发送失败处理方法
        auth_user: 发送者账号
        auth_password: 发送者授权码， EMAIL_HOST_PASSWORD
        connection: 连接方式
        html_message: html格式的邮件内容
    '''
    # try:
    send_mail('邮箱主题subject',
              '这里是文本内容message',
              settings.EMAIL_FROM,
              recipient_list=['786369470@qq.com'],
              html_message='<a href="#">haha</a>',
              fail_silently=True,
              )
    return HttpResponse('发送成功！')
    # except:
    #     return HttpResponse('出错啦！')


def up_img(request, *args):
    if request.method == 'GET':
        return render(request, 'blogapp/upload_img.html')
    elif request.method == 'POST':
        username = request.session.get('username')
        img = request.FILES.get('img')
        f2 = FileSystemStorage()
        path = f2.save('blog/%s'%(img.name), img)   # 保存文件并返回文件名，如果文件名存在则会创建一个不重复的名称
        user = Users.objects.get(username=username)
        user.photo = path
        user.save()
        print('上传头像成功！')
        return HttpResponseRedirect(f'/blog/person/')


def logout(request):
    # 清除session，删除用户信息
    request.session.flush()
    return HttpResponseRedirect('/blog/index/1')


# 设置返回状态码、cookie等
def response(request):
    # 设置cookie以及超时时间，默认为永不过期
    # return HttpResponse(content='ok', status=888).set_cookie('name', 'django', max_age=10)  # 超时时间为关闭后十秒钟
    # 超时时间为2019年8月14日0点0分
    return HttpResponse(content='ok', status=888).set_cookie('name',
                                                             'django',
                                                             expires=datetime(2019, 8, 14, 0, 0, 0))


# cookie登录
def cookie_login(request):
    uname = 'qqq'
    pword = 'qqq'
    username = request.POST.get('username')
    password = request.POST.get('password')
    if uname == username and pword == password:
        return HttpResponse('ok').set_cookie('username', uname)
    return render(request, '', {'username': username,
                                'password': password,
                                'is_login': False,
                                })


# 获取cookie等
def get_cookie(request):
    name = request.COOKIES.get('name')
    crsf = request.COOKIES.get('crsftoken')
    sessionid = request.COOKIES.get('sessionid')
    print(name, crsf, sessionid)
    return HttpResponse('OK')


# 清除cookie
def del_cookies(request):
    request.COOKIES.clear()     # 逻辑删除
    # response = HttpResponse.delete_cookie('name')

    return HttpResponse('删除cookie完成')


# 设置session信息
def set_session(request):
    request.session['name'] = 'blacky'
    request.session['name1'] = '诺克萨斯'
    # 设置超时时间，默认为两周，这里为20s,0表示关闭浏览器就删除session
    request.session.set_expiry(20)
    return HttpResponse('ok')


# 获取session信息
def get_session(request):
    name = request.session.get('name')
    name1 = request.session.get('name1')
    res = f"session信息:   name-{name}/name1-{name1}"
    return HttpResponse(res)


# 删除session
def del_session(request):
    request.session.clear()         # 删除值不删除键
    del request.session['name']     # 删除某个session
    request.session.flush()         # 完全删除session
    return HttpResponse('删除session完成')


# 视图类
class Index(ListView):
    model = Post                         # 模型类 Post.objects.all()
    template_name = 'blogapp/main.html'  # 模板
    context_object_name = 'p'            # 上下文

    def get_queryset(self):
        # 返回查询集
        print(self.args)
        return self.model.objects.get(id=self)

    def get_context_data(self, **kwargs):
        # 添加额外上下文
        # 获取父类上下文
        # context = super(Mark).get_context_data(**kwargs)
        # context['']
        pass