from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/choose/$', views.choose_name),   # 选择餐厅
    url(r'^/table/$', views.choose_table),   # 选择桌位
    url(r'^/newtable/$', views.add_table),        # 增加桌位
    url(r'^/client/(\d+)/$', views.client_num),        # 选择用餐人数
    url(r'^/p/(\d+)/$', views.menu),         # 菜单
    url(r'^/addfood/$', views.add_food),     # 新增菜品
    url(r'^/paying/$', views.paying),        # 支付页面
    url(r'^/check/$', views.check_paid),     # 检测是否支付
    url(r'^/wxpay/$', views.wx_pay),         # 微信支付
    url(r'^/admin/choose/$', views.adm_choose_canteen),            # 管理员页面-选择餐厅
    url(r'^/admin/change/(\d+)/$', views.adm_change_canteen),            # 管理员页面-选择修改餐厅信息
    url(r'^/admin/change/name/$', views.adm_change_name),            # 管理员页面-修改餐厅名字
    url(r'^/admin/change/boss/$', views.adm_change_boss),            # 管理员页面-修改餐厅主管
    url(r'^/admin/change/num/$', views.adm_change_num),            # 管理员页面-修改餐厅主管
    url(r'/admin/history/$', views.adm_history),                    # 管理员页面-查看商家订单
]
