from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'/choose/$', views.choose_name),
    url(r'/table/$', views.choose_table),
]
