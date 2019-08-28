from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/about/$', views.about),
    url(r'/index/(\d+)/$', views.index),
    url(r'/content/', views.content),
    url(r'/detail/(\d+)/$', views.detail),
    url(r'/friendly/$', views.friendly),
    url(r'/readerwall/$', views.reader_wall),
    url(r'/calc/$', views.calc),
]