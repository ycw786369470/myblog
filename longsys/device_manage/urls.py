from django.conf.urls import url
from device_manage import views, init_start

urlpatterns = [
    # url(r'^$', views.base),                                               # 基础页而
    url(r'^login/$', views.login, name='login'),                            # 登录
    url(r'^logout/$', views.logout, name='logout'),                         # 注销
    url(r'^regist/$', views.regist, name='regist'),                         # 注册
    url(r'^$', views.index, name='index'),                                  # 主页-选择设备类型
    url(r'^device/$', views.index_show, name='index_device'),               # 主页-展示设备
    url(r'^check_staff/$', views.check_staff),                              # 校验工号
    url(r'^choose_type/$', views.choose_type, name='choose'),               # 选择测试设备
    url(r'^choose_device/$', views.choose_device, name='choose_device'),    # 选择测试设备
    url(r'^device_details/$', views.device_details, name='device_details'),   # 设备详情
    url(r'^test_history/$', views.test_history, name='test_history'),       # 测试记录
    url(r'^history_detail/id/(\d+)$', views.history_detail, name='history_detail'),
    url(r'^new_demand/$', views.new_demand, name='new_demand'),             # 发起新需求
    url(r'^demand_device/$', views.demand_device, name='demand_device'),    # 选择任务设备
    url(r'^demand_choose/$', views.demand_choose, name='demand_choose'),    # ajax检测选择设备


    url(r'^manage_admin/$', views.admin, name='admin'),                         # 管理员
    url(r'^user_list/$', views.user_list, name='user_list'),                    # 人员管理
    url(r'^manage_devices/$', views.manage_devices, name='manage_devices'),     # 设备管理
    url(r'^add_device/$', views.add_device, name='add_device'),                 # 设备管理--添加设备
    url(r'^modify_device/$', views.modify_device, name='modify_device'),        # 修改设备信息
    url(r'^manage_demand/$', views.manage_demand, name='manage_demand'),        # 需求（任务）管理
    url(r'^allot_demand/$', views.allot_demand, name='allot_demand'),           # 分配需求（任务）
    url(r'^user_detail/id/(\d+)$', views.user_detail, name='user_detail'),      # 修改信息和权限
    url(r'^personal_home/$', views.personal_home, name='personal_home'),        # 用户个人中心
    url(r'^check_oldpwd/$', views.check_oldpwd, name='check_oldpwd'),
    url(r'^ajax_find/$', views.ajax_find_devices, name='ajax_find'),            # ajax异步搜索


    url(r'^device/search/$', views.Device_search.as_view(), name='device_search'),
    url(r'^device/search_list/$', views.Device_search.as_view(
        template_name='device_manage/base/device_load_list.html'
    ), name='device_load_list'),



    # 初始化
    url(r'^init/$', init_start.new_tpye),                   # 初始化数据
    url(r'^init_state/$', init_start.new_state),            # 初始化状态类
    url(r'^init_device/$', init_start.new_device),          # 添加示例设备
    url(r'^init_job/$', init_start.new_job),                # 初始化岗位类
    url(r'^init_group/$', init_start.new_group),            # 初始化小组类
    url(r'^init_record/$', init_start.new_test_record),     # 初始化测试记录
]
