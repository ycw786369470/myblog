from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from device_manage.models import *
import datetime
from django.http import JsonResponse
import hashlib
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.views.generic import ListView
from utils import constants
from django.core.files.storage import FileSystemStorage


# 获取用户信息
def get_msg(request):
    name = request.session.get('name')
    job = request.session.get('job')
    is_admin = request.session.get('is_admin')
    is_init = request.session.get('is_init')
    staff_number = request.session.get('staff_number')
    if name is None:
        name = '客户'
        job = '客户'
        is_admin = False
        is_init = False
    return name, job, is_admin, is_init, staff_number


# 筛选非空值
def get_value(value):
    if len(value) == 0:
        return '暂未填写'
    else:
        return value


# 主页--展示设备种类
def index(request):
    # 用户信息
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        # 设备信息
        d_type = DeviceType.objects.all()
        device_ls = [Device.objects.filter(device_type_id=i) for i in [t.id for t in d_type]]    # 对应设备
        sum_ls = [len(i) for i in device_ls]
        usable_ls = [len(i.filter(device_state__state='可使用')) for i in device_ls]
        unite_ls = []
        for i in range(len(d_type)):
            unite_ls.append([
                d_type[i].id,
                d_type[i].device_type,
                d_type[i].device_intro,
                sum_ls[i],
                usable_ls[i]
            ])
        txt = {
            'unite_ls': unite_ls,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/base/index.html', txt)


# 初始页面，展示某种类型的设备
def index_show(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        id = request.GET.get('id')
        devices = Device.objects.filter(device_type_id=id)
        total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))     # 分类查询个数
        total_dict = {}
        for d in total_num:
            total_dict[d.get('device_spec')] = d.get('device_spec__count')
        device_type = DeviceType.objects.get(id=id)
        page = int(request.GET.get('page', 1))
        page_size = 15
        num_list = [i for i in range(page_size * (int(page) - 1) + 1, (page_size * (int(page))) + 1)]  # 序号列表
        paginator = Paginator(devices, page_size)
        page_data = paginator.page(page)  # 分好的数据
        page_data_list = [item for item in page_data.object_list]  # 页面中的数据集
        num_page_data_list = [(num_list[i], page_data_list[i], total_dict.get(page_data_list[i].device_spec)) for i in range(len(page_data_list))]  # 页面数据带序号列表
        page_nums = paginator.num_pages  # 页码总数量
        if page_nums >= 4:
            if page + 4 > page_nums:
                page_num_list = [p for p in range(page_nums - 3, page_nums + 1)]  # 页码列表
            else:
                page_num_list = [p for p in range(page, page + 4)]
        else:
            page_num_list = [p for p in range(1, page_nums + 1)]
        type_name = DeviceType.objects.get(id=id)  # 获取该设备对应类别信息
        title = type_name.device_type  # 获取类别中的类别名
        txt = {
            'id': id,
            'page': page,
            'page_nums': page_nums,
            'page_num_list': page_num_list,
            'page_data': page_data,
            'num_page_data_list': num_page_data_list,
            'title': title,
            'type': device_type,
            'devices': devices,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/base/index_show.html', txt)


def choose_type(request):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        # 设备信息
        d_type = DeviceType.objects.all()
        device_ls = [Device.objects.filter(device_type_id=i) for i in [t.id for t in d_type]]    # 对应设备
        sum_ls = [len(i) for i in device_ls]
        usable_ls = [len(i.filter(device_state__state='可使用')) for i in device_ls]
        unite_ls = []
        for i in range(len(d_type)):
            unite_ls.append([
                d_type[i].id,
                d_type[i].device_type,
                d_type[i].device_intro,
                sum_ls[i],
                usable_ls[i]
            ])
        txt = {
            'unite_ls': unite_ls,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/tester/choose_type.html', txt)


def choose_device(request):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        id = request.GET.get('id')
        devices = Device.objects.filter(device_type_id=id)
        total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))     # 分类查询个数
        total_dict = {}
        for d in total_num:
            total_dict[d.get('device_spec')] = d.get('device_spec__count')
        device_type = DeviceType.objects.get(id=id)
        page = int(request.GET.get('page', 1))
        page_size = 15
        num_list = [i for i in range(page_size * (int(page) - 1) + 1, (page_size * (int(page))) + 1)]  # 序号列表
        paginator = Paginator(devices, page_size)
        page_data = paginator.page(page)  # 分好的数据
        page_data_list = [item for item in page_data.object_list]  # 页面中的数据集
        num_page_data_list = [(num_list[i], page_data_list[i], total_dict.get(page_data_list[i].device_spec)) for i in range(len(page_data_list))]  # 页面数据带序号列表
        page_nums = paginator.num_pages  # 页码总数量
        if page_nums >= 4:
            if page + 4 > page_nums:
                page_num_list = [p for p in range(page_nums - 3, page_nums + 1)]  # 页码列表
            else:
                page_num_list = [p for p in range(page, page + 4)]
        else:
            page_num_list = [p for p in range(1, page_nums + 1)]
        type_name = DeviceType.objects.get(id=id)  # 获取该设备对应类别信息
        title = type_name.device_type  # 获取类别中的类别名
        txt = {
            'id': id,
            'page': page,
            'page_nums': page_nums,
            'page_num_list': page_num_list,
            'page_data': page_data,
            'num_page_data_list': num_page_data_list,
            'title': title,
            'type': device_type,
            'devices': devices,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/tester/choose_device.html', txt)


def device_details(request):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        d_id = request.GET.get('device')    # 设备id号
        device = Device.objects.get(id=d_id)
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            "device": device,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/base/device_details.html', txt)


# 查看测试记录
def test_history(request):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        if is_admin: # 如果是管理员可查看所有测试记录
            test_history = TestRecord.objects.all()
        else:        # 非管理员只能查看自己个人测试记录
            try:
                user = User.objects.filter(staff_number=staff_number)[0]
                user_id = user.id
                test_history = TestRecord.objects.filter(user_id=user_id)
            except:
                test_history = []
        history_list = []
        if len(test_history) != 0:
            for h in test_history:
                h_id = h.id
                h_user = User.objects.filter(id=h.user_id)[0].name
                h_device = Device.objects.filter(id=h.device_id)[0]
                h_version = h.version
                h_match = h.match
                h_card_num = h.card_num
                h_card_id = h.card_id
                history_list.append(
                    [h_id,h_device,h_user,h_version,h_match,h_card_num,h_card_id]
                )
        # 记录显示进行分页
        page = request.GET.get('page')
        page_size = 15
        paginator = Paginator(history_list, page_size)
        page_data = paginator.page(page)  # 分好的数据
        txt = {
            'page': page,
            'history_ls': page_data,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/admin/test_history.html', txt)


# 测试记录详情
def history_detail(request, index):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        history = TestRecord.objects.filter(id=index)[0]
        txt = {
            'history': history,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/admin/history_detail.html', txt)


def new_demand(request):
    name, job, is_admin, is_init,staff_number = get_msg(request)
    if request.method == 'GET':
        # 设备信息
        d_type = DeviceType.objects.all()
        device_ls = [Device.objects.filter(device_type_id=i) for i in [t.id for t in d_type]]    # 对应设备
        sum_ls = [len(i) for i in device_ls]
        usable_ls = [len(i.filter(device_state__state='可使用')) for i in device_ls]
        unite_ls = []
        for i in range(len(d_type)):
            unite_ls.append([
                d_type[i].id,
                d_type[i].device_type,
                d_type[i].device_intro,
                sum_ls[i],
                usable_ls[i]
            ])
        txt = {
            'unite_ls': unite_ls,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/demander/demand_type.html', txt)


def demand_device(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        id = request.GET.get('id')
        devices = Device.objects.filter(device_type_id=id)
        total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))  # 分类查询个数
        total_dict = {}
        for d in total_num:
            total_dict[d.get('device_spec')] = d.get('device_spec__count')
        device_type = DeviceType.objects.get(id=id)
        num_list = [i for i in range(1, len(devices)+1)]  # 序号列表
        num_page_data_list = [(num_list[i], devices[i], total_dict.get(devices[i].device_spec)) for i in
                              range(len(devices))]  # 页面数据带序号列表
        type_name = DeviceType.objects.get(id=id)  # 获取该设备对应类别信息
        title = type_name.device_type  # 获取类别中的类别名
        txt = {
            'id': id,
            'num_page_data_list': num_page_data_list,
            'title': title,
            'type': device_type,
            'devices': devices,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/demander/demand_device.html', txt)


def admin(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
        }
        return render(request, 'device_manage/admin/manage_admin.html', txt)


def demand_choose(request):
    if request.method == 'POST':
        id_ls = request.POST.getlist('id_ls[]')
        device_ls = id_ls
        return HttpResponse(id_ls)


def check_staff(request):
    staff = request.POST.get("staff")
    user = User.objects.filter(staff_number=staff)
    if user:
        return JsonResponse({"erro": 1})
    else:
        return JsonResponse({"erro": 0})


# 登录
def login(request):
    if request.method == "GET":
        # 检测浏览器的cookie中是否存在用户信息
        if ('staff_number' in request.COOKIES) and ('pwd' in request.COOKIES):
            staff_number = request.COOKIES.get('staff_number').encode('iso-8859-1').decode('utf-8')
            password = request.COOKIES.get('pwd')
        else:
            staff_number = ''
            password = ''
        return render(request, 'device_manage/base/login.html', context={'staff_number': staff_number, 'pwd': password})
    elif request.method == "POST":
        login_form = request.POST
        staff_number = login_form.get('staff_number')
        password = login_form.get('password')
        user = User.objects.filter(staff_number=staff_number)
        # 对输入密码进行加密
        s = hashlib.sha1()
        s.update(password.encode('utf-8'))
        s_pwd = s.hexdigest()
        if not user:
            msg = '用户不存在'
            return render(request, 'device_manage/base/login.html', context={'point_out':msg})
        else:
            if s_pwd != user[0].password:
                msg = '密码错误'
                return render(request, 'device_manage/base/login.html', context={'point_out': msg})
            # 获取当前登录时间
            u = User.objects.get(staff_number=staff_number)
            u.last_login = datetime.datetime.now()
            u.save()
            rep = redirect('/')
            request.session['name'] = u.name
            request.session['staff_number'] = u.staff_number
            request.session['job'] = u.job.job_name
            request.session['is_admin'] = u.is_admin
            request.session['is_init'] = u.is_init
            remember = login_form.get('remember')
            if remember:
                # 设置cookie，过期时间为一周
                rep.set_cookie('pwd', password, max_age=7*24*3600)
                rep.set_cookie('staff_number', bytes(staff_number, 'utf-8').decode('iso-8859-1'), max_age=7*24*3600)
            return rep


# 注册
def regist(request):
    # 获取数据库中的分组信息
    group_all = Group.objects.all()
    group_list = []
    for group in group_all:
        group_dict = {}
        group_dict['id'] = group.id
        group_dict['name'] = group.group_name
        group_list.append(group_dict)
    # 获取数据库中的岗位信息
    job_all = Job.objects.all()
    job_list = []
    for job in job_all:
        job_dict = {}
        job_dict['id'] = job.id
        job_dict['name'] = job.job_name
        job_list.append(job_dict)
    if request.method == 'GET':
        return render(request, 'device_manage/base/register.html', context={'group_list': group_list, 'job_list': job_list})
    elif request.method == 'POST':
        reg_form = request.POST
        password = reg_form.get('password')         # 密码
        check_password = reg_form.get('check_password')     # 确认密码
        name = reg_form.get('name')                 # 姓名
        number = reg_form.get('number')             # 工号
        try:
            group_choose = reg_form.get('group')
            group_value = Group.objects.get(id=group_choose)     # 分组
            job_choose = reg_form.get('job')
            job_value = Job.objects.get(id=job_choose)          # 岗位
        except:
            group_value = ''
            job_value = ''
        if not (password and check_password and name and number and group_value and job_value):
            msg = '注册信息填写不完整'
            return render(request, 'device_manage/base/register.html', context={'point_out':msg, 'group_list':group_list, 'job_list':job_list})
        else:
            # 密码加密
            s = hashlib.sha1()
            s.update(password.encode('utf-8'))
            sha1_pwd = s.hexdigest()
            # 写入数据库
            regist_time = datetime.datetime.now()
            c_is_init = reg_form.get('is_init')
            is_init = False
            if c_is_init:
                is_init = True
            u = User(password=sha1_pwd, group=group_value, job=job_value, name=name, staff_number=number,
                     regist_time=regist_time, is_init=is_init)
            u.save()
            request.session['name'] = name
            request.session['job'] = u.job.job_name
            request.session['is_admin'] = u.is_admin
            request.session['is_init'] = u.is_init
            return redirect('/')


# 注销(清除session)
def logout(request):
    request.session.flush()
    return redirect('/')


class Device_search(ListView):
    """" 设备列表 """
    # 每页放多少条数据
    paginate_by = constants.PAGE_SIZE
    # 模板位置
    template_name = 'device_manage/base/device_search.html'

    def get_queryset(self):
        # 判断session中的身份
        identity = self.request.session.get('name')
        # 按名称搜索
        name = self.request.GET.get('name', '')
        query = Q(device_brand__icontains=name)
        if len(Device.objects.filter(query)) == 0:
            query = Q(device_support__icontains=name)
        elif len(Device.objects.filter(query)) == 0:
            query = Q(device_begin__icontains=name)
        elif len(Device.objects.filter(query)) == 0:
            query = Q(device_card__icontains=name)
        elif len(Device.objects.filter(query)) == 0:
            return False
        return Device.objects.filter(query)

    def get_context_data(self, **kwargs):
        """ 添加额外的参数, 添加搜索参数 """
        context = super().get_context_data(**kwargs)
        # context['search_name'] = self.request.GET.get('name', '')
        context['search_data'] = self.request.GET.dict()
        return context


# 管理员用户管理
def user_list(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    user_list = User.objects.all()
    # 记录显示进行分页
    page = request.GET.get('page')
    page_size = 15
    paginator = Paginator(user_list, page_size)
    page_data = paginator.page(page)  # 分好的数据
    txt = {
        'page': page,
        'user_list': page_data,
        'name': name,
        'job': job,
        'is_admin': 1 if is_admin else 0,
        'is_init': 1 if is_init else 0,
        'staff_number': staff_number,
    }
    return render(request, 'device_manage/admin/user_list.html', txt)


def manage_devices(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    # 获取设备总数
    d_type = DeviceType.objects.all()
    device_ls = [Device.objects.filter(device_type_id=i) for i in [t.id for t in d_type]]  # 对应设备
    sum_ls = [len(i) for i in device_ls]
    total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))  # 分类查询个数
    total_dict = {}
    for d in total_num:
        total_dict[d.get('device_spec')] = d.get('device_spec__count')
    if request.method == 'GET':
        devices = Device.objects.all()
        num_list = [i for i in range(1, len(devices)+1)]  # 序号列表
        data_list = [(num_list[i], devices[i], total_dict.get(devices[i].device_spec)) for i in range(len(devices))]  # 页面数据带序号列表
        txt = {
            'num_page_data_list': data_list,
            'devices': devices,
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
            'sum': sum_ls,
        }
        return render(request, 'device_manage/admin/manage_devices.html', txt)


# 新增设备
def add_device(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        device_types = DeviceType.objects.all()
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
            'type': device_types,
        }
        return render(request, 'device_manage/admin/add_device.html', txt)
    elif request.method == 'POST':
        state = State.objects.get(state='可使用')
        type = request.POST.get('type')
        d_type = DeviceType.objects.get(device_type=type)
        d_id = request.POST.get('brand')
        brand = request.POST.get('device_id')
        spec = request.POST.get('spec')
        year = int(request.POST.get('year'))
        support = request.POST.get('support')
        fw = request.POST.get('fw')
        CPU = request.POST.get('CPU')
        card = request.POST.get('card')
        slog = request.POST.get('slog')
        card_capacity = request.POST.get('card_capacity')
        sys = request.POST.get('sys')
        i_format = request.POST.get('img_format')
        i_avg = request.POST.get('img_speed')
        v_format = request.POST.get('video_format')
        v_speed = request.POST.get('video_speed')
        v_max = request.POST.get('video_max')
        v_cut = request.POST.get('video_cut')
        speed = request.POST.get('speed')
        max_reso = request.POST.get('max_reso')
        character = request.POST.get('character')
        temper = get_value(request.POST.get('temper'))
        vol_ele = get_value(request.POST.get('vol_ele'))
        card_vol = get_value(request.POST.get('vol_ele'))
        p_id = get_value(request.POST.get('vol_ele'))
        p_belong = get_value(request.POST.get('pro_belong'))
        begin = get_value(request.POST.get('begin'))
        price = request.POST.get('price')
        camera_num = request.POST.get('camera_num')
        per_img = request.FILES.get('img')
        if per_img:
            f = FileSystemStorage()
            per_img = f.save('media/%s'%(per_img.name), per_img)
        else:
            per_img = '暂未上传'
        new_device = Device()
        self = new_device.add_device(
            d_type, d_id, brand, spec, year, support,
            fw, CPU, card, slog, card_capacity, sys, i_format,
            i_avg, v_format, v_speed, v_max, v_cut,
            speed, max_reso, camera_num, temper, vol_ele, card_vol,
            per_img, character, state, p_id, begin, p_belong, price
        )
        self.save()
        return redirect('/manage_devices/')


def modify_device(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    d_id = request.GET.get('id')
    device = Device.objects.get(id=d_id)
    if request.method == 'GET':
        device_types = DeviceType.objects.all()
        device_state = State.objects.all()
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
            'device': device,
            'type': device_types,
            'state': device_state,
        }
        return render(request, 'device_manage/admin/modify_device.html', txt)
    elif request.method == 'POST':
        d_state = request.POST.get('state')
        d_type = request.POST.get('type')
        device.device_state = State.objects.get(state=d_state)
        device.device_type = DeviceType.objects.get(device_type=d_type)
        device.device_id = request.POST.get('device_id')
        device.device_brand = request.POST.get('brand')
        device.device_spec = request.POST.get('spec')
        device.device_year = int(request.POST.get('year'))
        device.device_support = request.POST.get('support')
        device.device_fw_ver = request.POST.get('fw')
        device.CPU = request.POST.get('CPU')
        device.device_card = request.POST.get('card')
        device.device_card_slog = request.POST.get('slog')
        device.device_card_capacity = request.POST.get('card_capacity')
        device.sys = request.POST.get('sys')
        device.device_img_format = request.POST.get('img_format')
        device.device_img_avg = request.POST.get('img_speed')
        device.device_video_format = request.POST.get('video_format')
        device.device_video_speed = request.POST.get('video_speed')
        device.device_video_max = request.POST.get('video_max')
        device.device_video_cut = request.POST.get('video_cut')
        device.device_speed = request.POST.get('speed')
        device.device_max_reso = request.POST.get('max_reso')
        device.device_character = request.POST.get('character')
        device.device_temper = get_value(request.POST.get('temper'))
        device.voltage_electric = get_value(request.POST.get('vol_ele'))
        device.card_voltage = get_value(request.POST.get('card_vol'))
        device.device_property_id = get_value(request.POST.get('pro_id'))
        device.device_property_belong = get_value(request.POST.get('pro_belong'))
        device.device_begin = get_value(request.POST.get('begin'))
        device.price = request.POST.get('price')
        device.device_camera_num = request.POST.get('camera_num')
        per_img = request.FILES.get('img')
        if per_img:
            f = FileSystemStorage()
            per_img = f.save('media/%s' %(per_img.name), per_img)
            device.device_per_img = per_img
        device.save()
        return redirect('/manage_devices/')


def manage_demand(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        requirements = TestRequirements.objects.all()
        devices = []
        for r in requirements:
            devices.append([len(r.device.split('/')), r])
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
            'devices': devices,
        }
        return render(request, 'device_manage/admin/manage_demand.html', txt)


def allot_demand(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    if request.method == 'GET':
        r_id = request.GET.get('rid')   # 获取任务号
        require = TestRequirements.objects.get(id=r_id)
        d_id = require.device.split('/')                    # 对应device的id
        d_ls = []                                           # 根据id找到对应device列表
        for d in d_id:
            device = Device.objects.get(id=d)
            print('任务id：', r_id, '设备id：', d)
            allot = RequirementsRecord.objects.filter(Q(task_id=r_id) | Q(device_id=d))
            if allot:
                d_ls.append([device, allot[0].allot])
            else:
                d_ls.append([device, None])
        txt = {
            'name': name,
            'job': job,
            'is_admin': 1 if is_admin else 0,
            'is_init': 1 if is_init else 0,
            'staff_number': staff_number,
            'devices': d_ls,
        }
        return render(request, 'device_manage/admin/allot_demand.html', txt)


# 管理员查看用户信息详情或修改用户信息
def user_detail(request, index):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    user = User.objects.filter(id=index)[0]
    # 获取数据库中的分组信息
    group_all = Group.objects.all()
    group_list = []
    for group in group_all:
        group_dict = {}
        group_dict['id'] = group.id
        group_dict['name'] = group.group_name
        group_list.append(group_dict)
    # 获取数据库中的岗位信息
    job_all = Job.objects.all()
    job_list = []
    for job in job_all:
        job_dict = {}
        job_dict['id'] = job.id
        job_dict['name'] = job.job_name
        job_list.append(job_dict)
    txt = {
        'user': user,
        'name': name,
        'job': job,
        'group_list': group_list,
        'job_list': job_list,
        'is_admin': 1 if is_admin else 0,
        'is_init': 1 if is_init else 0,
        'staff_number': staff_number,
    }
    if request.method == 'GET':
        return render(request, 'device_manage/admin/user_detail.html', txt)
    elif request.method == 'POST':
        modify_form = request.POST
        new_name = modify_form.get('name')  # 姓名
        new_number = modify_form.get('number')  # 工号
        group_choose = modify_form.get('group')
        new_group_value = Group.objects.get(id=group_choose)  # 分组
        job_choose = modify_form.get('job')
        new_job_value = Job.objects.get(id=job_choose)  # 岗位
        new_is_admin = int(modify_form.get('admin'))
        new_is_init = int(modify_form.get('init'))
        # 将用户信息更新为修改后的信息
        user = User.objects.filter(id=index)[0]
        user.name = new_name
        user.staff_number = new_number
        user.group = new_group_value
        user.job = new_job_value
        user.is_init = new_is_init
        user.is_admin = new_is_admin
        user.save()
        return redirect('/user_list/?page=1')


# ajax异步搜索
def ajax_find_devices(request):
    # 获取设备总数
    total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))  # 分类查询个数
    total_dict = {}
    for d in total_num:
        total_dict[d.get('device_spec')] = d.get('device_spec__count')
    if request.method == 'POST':
        # 通过类型选择种类
        if request.POST.get('way') == 'type':
            types = request.POST.getlist('types[]')
            devices = []
            for i in types:
                d = Device.objects.filter(device_type__device_type=i)
                for j in d:
                    devices.append([total_dict.get(j.device_spec), j])
            txt = {
                'devices': devices,
            }
            data = render_to_string('device_manage/base/ajax_find_devices.html', txt)
            return HttpResponse(data)
        # 通过编号、型号搜索
        else:
            input_txt = request.POST.get('input')
            devices = []
            device = Device.objects.filter(device_id=input_txt)
            for d in device:
                devices.append([total_dict.get(d.device_spec), d])
            if len(devices) == 0:
                device = Device.objects.filter(device_spec=input_txt)
                for d in device:
                    devices.append([total_dict.get(d.device_spec), d])
            txt = {
                'devices': devices,
                'input': input_txt,
            }
            data = render_to_string('device_manage/base/ajax_find_devices.html', txt)
            return HttpResponse(data)


# 用户个人中心
def personal_home(request):
    name, job, is_admin, is_init, staff_number = get_msg(request)
    index = request.GET.get('id')
    user = User.objects.filter(staff_number=index)[0]
    txt = {
        'name': name,
        'job': job,
        'user': user,
        'staff_number': staff_number,
        'is_admin': 1 if is_admin else 0,
        'is_init': 1 if is_init else 0,
    }
    if request.method == 'GET':
        return render(request, 'device_manage/admin/personal_home.html', txt)
    elif request.method == 'POST':
        new_pwd = request.POST.get('new_pwd')
        if new_pwd != '':
            # 加密
            s = hashlib.sha1()
            s.update(new_pwd.encode('utf-8'))
            s_pwd = s.hexdigest()
            user.password = s_pwd
            user.save()
            return render(request, 'device_manage/admin/personal_home.html', txt)


# 修改密码时校验原密码是否正确
def check_oldpwd(request):
    print('**********')
    old_pwd = request.POST.get('pwd')
    page_url = request.POST.get('url')
    index = page_url.split('=')[-1]
    password = User.objects.filter(staff_number=index)[0].password
    s = hashlib.sha1()
    s.update(old_pwd.encode('utf-8'))
    s_pwd = s.hexdigest()
    if s_pwd == password:
        return JsonResponse({"erro":0})
    else:
        return JsonResponse({"erro":1})








