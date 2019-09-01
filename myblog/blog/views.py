from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import datetime
from django.utils import timezone
from blogapp.models import *
import math
from datetime import timedelta
from django.db.models import F,Q
from django.views.generic import ListView
# Create your views here.


def about(request):
    return render(request, 'blog/about.html')


def content(request):
    return render(request, 'blog/content.html')


def message(request):
    # 观看博客者的username
    username = request.session.get('username')
    if username == None:
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
    # 前五条评论
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


class Index(ListView):
    model = BlogUser
    template_name = 'blog/index.html'

    def get_queryset(self):
        return super(Index, self).get_queryset()

    def get_context_data(self, **kwargs):
        '''
        获取上下文
            :param kwargs:
            :return:
        '''
        pass


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
                return HttpResponseRedirect('/main/index/1')
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
    now_time = datetime.date.today()
    this_week = now_time.isoweekday()
    all_blogs = BlogUser.objects.all()
    all_comment = Comment.objects.all()
    new_blogs = all_blogs[0:5]
    # 热门评论
    comment = all_comment[0:5]
    # 当前博客文章
    num = args[0]
    blog = BlogUser.objects.get(id=num)
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
        if mark_up.is_over == False:
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
        if mark_down.is_over == False:
            mark_down.is_over = True
            mark_down.save()
            mark_num = mark.down_num + 1
            mark.down_num = mark_num
        else:
            mark_num = mark.down_num
    mark.save()
    # 给ajax返回success
    return HttpResponse(mark_num)


def reader_wall(request):
    return render(request, 'blog/readerWall.html')


