from django.conf.urls import url
from device_manage import views, init_start, views_base, views_admin, views_tester, views_demander


urlpatterns = [
    # views_base
    url(r'^login/$', views_base.login, name='login'),                            # 登录
    url(r'^logout/$', views_base.logout, name='logout'),                         # 注销
    url(r'^regist/$', views_base.regist, name='regist'),                         # 注册
    url(r'^$', views_base.index, name='index'),                                  # 主页-选择设备类型
    url(r'^device/$', views_base.index_show, name='index_device'),               # 主页-展示设备
    url(r'^check_staff/$', views_base.check_staff),                              # 校验工号
    url(r'^test_history/$', views_admin.test_history, name='test_history'),      # 测试记录
    url(r'^history_detail/id/(\d+)/page/(\d+)$', views_admin.history_detail, name='history_detail'),
    url(r'^personal_home/$', views_base.personal_home, name='personal_home'),    # 用户个人中心
    url(r'^check_oldpwd/$', views_base.check_oldpwd, name='check_oldpwd'),
    url(r'^parts$', views_base.show_parts, name='parts'),                        # 查看配件
    url(r'^about$', views_base.about, name='about'),                             # 关于页面
    url(r'^index2$', views_base.index_flush, name='index_flush'),                # 嵌入式主页

    # views_admin
    url(r'^user_list/$', views_admin.user_list, name='user_list'),                # 人员管理
    url(r'^manage_devices/$', views_admin.manage_devices, name='manage_devices'), # 设备管理
    url(r'^filter_data/$', views_admin.filter_data, name='filter'),               # 筛选设备
    url(r'^device_detail/$', views_admin.device_detail, name='device_detail'),    # 设备管理
    url(r'^add_device/$', views_admin.add_device, name='add_device'),             # 设备管理--添加设备
    url(r'^many_devices/$', views_admin.many_devices, name='many_devices'),       # 设备管理--批量添加
    url(r'^change_type/$', views_admin.change_type, name='change_type'),          # 设备管理--改变表单
    url(r'^delete_device/$', views_admin.delete_device, name='delete_device'),    # 设备管理--改变表单
    url(r'^modify_device/$', views_admin.modify_device, name='modify_device'),    # 修改设备信息
    url(r'^device_record/$', views_admin.device_record, name='device_record'),    # 查看设备历史测试记录
    url(r'^reject_demand/$', views_admin.reject_demand, name='reject_demand'),    # 分配需求（任务）
    url(r'^allot_demand/$', views_admin.allot_demand, name='allot_demand'),       # 分配需求（任务）
    url(r'^user_detail/id/(\d+)$', views_admin.user_detail, name='user_detail'),  # 修改信息和权限
    url(r'^ajax_find/$', views_admin.ajax_find_devices, name='ajax_find'),        # ajax异步搜索设备
    url(r'^search_user/$', views_admin.search_user, name='search_user'),          # 管理员搜索用户
    url(r'^card_num_sort/$', views_admin.card_num_sort, name='card_num_sort'),    # 测试记录通过卡数量排序
    url(r'^add_parts/$', views_admin.add_parts, name='add_parts'),                # 添加配件
    url(r'^modify_parts/$', views_admin.modify_parts, name='modify_parts'),       # 修改配件
    url(r'^choose_result/id/(\d+)$', views_admin.choose_result, name='choose_result'),
    url(r'^export_record/id/(\d+)$', views_admin.export_record, name='export_record'),
    url(r'^choose_match/$', views_admin.choose_match, name='choose_match'),


    # tester
    url(r'^manage_demand/$', views_admin.manage_demand, name='manage_demand'),     # 需求（任务）管理
    url(r'^personal_task/$', views_tester.personal_task, name='personal_task'),    # 个人任务
    url(r'^task_detail/$', views_tester.task_detail, name='task_detail'),          # 开始任务详情
    url(r'^record_result/$', views_tester.record_result, name='record_result'),    # 记录测试结果，选择设备
    url(r'^check_finish/$', views_tester.check_finish, name='check_finish'),       # 提交任务
    url(r'^check_allotted/$', views.check_allotted, name='check_allotted'),        # 查找未分配需求的数量

    # demander
    url(r'^new/requirements/$', views_demander.New_built.as_view(), name='new_built'),
    url(r'^release/task/$', views_demander.release_task, name='release_task'),               # 保存到数据库
    url(r'^sample/info/$', views_demander.sample_info, name='sample_info'),                  # 样品数据
    url(r'^demand/recoder/$', views_demander.demand_recoder, name='demand_recoder'),         # 需求记录
    url(r'^demand/recoder/detail/$', views_demander.demand_recoder_detail, name='demand_recoder_detail'),   # 记录详情
    url(r'^device/search/$', views_demander.Device_search.as_view(), name='device_search'),  # 搜索设备
    url(r'^reset_match/$', views_demander.reset_match, name='reset_match'),                  # 修改搭配
    url(r'^reset_ver/$', views_demander.reset_ver, name='reset_ver'),                        # 修改版本
    url(r'^new_demand/$', views_demander.new_demand, name='new_demand'),                     # 发起新需求
    url(r'^device/search_list/$', views_demander.Device_search.as_view(  # 搜索设备
        template_name='device_manage/base/device_load_list.html'
    ), name='device_load_list'),
    url(r'^new/load_list/$', views_demander.New_built.as_view(
        template_name='device_manage/demander/new_built_load_list.html'
    ), name='new_load_list'),
    url(r'^new/demand/$', views_demander.New_built.as_view(
        template_name='device_manage/demander/new_demand.html'
    ), name='new_demand'),                                                                   # 新建需求

    # 初始化   
    url(r'^init/$', init_start.new_tpye),                                   # 初始化数据
    url(r'^init_state/$', init_start.new_state),                            # 初始化状态类
    url(r'^init_device/$', init_start.new_device),                          # 添加示例设备
    url(r'^init_job/$', init_start.new_job),                                # 初始化岗位类
    url(r'^init_group/$', init_start.new_group),                            # 初始化小组类
    url(r'^init_record/$', init_start.new_test_record),                     # 初始化测试记录
    url(r'^new_history/$', init_start.new_history),                         # 初始化测试记录
    url(r'^new_task/$', init_start.new_task),                               # 初始化个人任务
    url(r'^init_all/$', init_start.all_do),                                 # 全部初始化
    url(r'^init_SN/$', init_start.add_SN),                                  # 初始化SN表
]
