from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/about/$', views.about),
    url(r'/index/(\d+)/$', views.index),
    url(r'/content/', views.content),
    url(r'/detail/(\d+)/$', views.detail),
    url(r'/message/$', views.message),
    url(r'/calc/$', views.calc),
    url(r'/login/$', views.login),
    url(r'/register/$', views.register),
    url(r'/person/$', views.person),
    url(r'/addblog/$', views.addblog),
]
