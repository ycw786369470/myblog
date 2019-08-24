from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.main, name='main'),                        # 访问主页
    url(r'/blog/(\d+)', views.blog, name='blog'),              # 博客
    url(r'/addblog/username=(.*)', views.add_blog, name='addblog'),         # 新增博客
    url(r'/addblogok/$', views.add_blog_ok, name='addblogok'),
    url(r'/comment/(\d+)/username=(.*)', views.comment, name='comment'),          # 详情页
    url(r'/test/$', views.get_info),
    url(r'/calc/$', views.calc),
    url(r'/login_test/$', views.cookie_login),
    url(r'/setsession/$', views.set_session),
    url(r'/getsession/$', views.get_session),
    url(r'/listview/$', views.Index.as_view()),
    url(r'/base/$', views.base),
    url(r'/login/$', views.login),
    url(r'/register/$', views.register),
    url(r'/registering/$', views.registering),
    url(r'/person/username=(.*)$', views.person),
    url(r'/sendmsg/$', views.send_msg),
    url(r'/img/username=(.*)$', views.up_img),
    url(r'/logout/$', views.logout),
]
