from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/choose/$', views.choose_name),
    url(r'/table/$', views.choose_table),
    url(r'/add/$', views.add_table),
    url(r'/p/(\d+)/$', views.menu),
    url(r'/addfood/$', views.add_food),
]
