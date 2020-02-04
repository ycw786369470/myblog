from device_manage.views import *


# 登录
def login(request):
    if request.method == "GET":
        # 检测浏览器的cookie中是否存在用户信息
        if ('email' in request.COOKIES) and ('pwd' in request.COOKIES):
            email = request.COOKIES.get('email').encode('iso-8859-1').decode('utf-8')
            password = request.COOKIES.get('pwd')
        else:
            email = ''
            password = ''
        return render(request, 'device_manage/base/login.html', context={'email': email, 'pwd': password})
    elif request.method == "POST":
        login_form = request.POST
        email = login_form.get('email')
        password = login_form.get('password')
        user = User.objects.filter(email=email)
        # 对输入密码进行加密
        s = hashlib.sha1()
        s.update(password.encode('utf-8'))
        s_pwd = s.hexdigest()
        if not user:
            msg = '该邮箱未注册'
            return render(request, 'device_manage/base/login.html', context={'point_out':msg})
        else:
            if s_pwd != user[0].password:
                msg = '密码错误'
                return render(request, 'device_manage/base/login.html', context={'point_out': msg})
            # 获取当前登录时间
            u = User.objects.get(email=email)
            u.last_login = datetime.datetime.now()
            u.save()
            rep = redirect('/')
            request.session['name'] = u.name
            request.session['staff_number'] = u.staff_number
            request.session['job'] = u.job.job_name
            request.session['is_admin'] = u.is_admin
            request.session['is_init'] = u.is_init
            request.session['email'] = u.email
            remember = login_form.get('remember')
            if remember:
                # 设置cookie，过期时间为一周
                rep.set_cookie('pwd', password, max_age=7*24*3600)
                rep.set_cookie('email', bytes(email, 'utf-8').decode('iso-8859-1'), max_age=7*24*3600)
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
        name = reg_form.get('name')                 # 姓名
        user_ls = User.objects.all()
        name_ls = []
        for u in user_ls:
            name_ls.append(u.name)
        cnt = 1
        name1 = name
        while True:
            if name in name_ls:
                name = name1 + str(cnt)
                cnt += 1
                continue
            else:
                break
        number = reg_form.get('number')             # 工号
        email = reg_form.get('email')               # 邮箱
        try:
            group_choose = reg_form.get('group')
            group_value = Group.objects.get(id=group_choose)     # 分组
            job_choose = reg_form.get('job')
            job_value = Job.objects.get(id=job_choose)          # 岗位
        except:
            group_value = ''
            job_value = ''

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
                 regist_time=regist_time, is_init=is_init,email=email)
        u.save()
        request.session['name'] = name
        request.session['staff_number'] = u.staff_number
        request.session['job'] = u.job.job_name
        request.session['is_admin'] = u.is_admin
        request.session['is_init'] = u.is_init
        return redirect('/')


# 注销(清除session)
def logout(request):
    save_action(request, '注销登陆')
    request.session.flush()
    return redirect('/')


# 主页--展示设备种类
def index(request):
    if request.method == 'GET':
        if request.session.get('name') is not None:
            save_action(request, '访问主页')
        # 设备信息
        d_type = DeviceType.objects.all()
        device_ls = [Device.objects.filter(Q(device_type_id=i), Q(is_delete=False)) for i in [t.id for t in d_type]]    # 对应设备
        sum_ls = [len(i) for i in device_ls]
        usable_ls = [len(i.filter(device_state__state='可使用')) for i in device_ls]
        unite_ls = []
        for i in range(len(d_type)):
            unite_ls.append([
                d_type[i],
                sum_ls[i],
                usable_ls[i]
            ])
        txt = {
            'unite_ls': unite_ls,
        }
        return render(request, 'device_manage/base/index.html', txt)


# 初始页面，展示某种类型的设备
def index_show(request):
    if request.method == 'GET':
        if request.session.get('name') is not None:
            save_action(request, '访问设备展示页面')
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
        }
        return render(request, 'device_manage/base/index_show.html', txt)


def check_staff(request):
    staff = request.POST.get("staff")
    user = User.objects.filter(staff_number=staff)
    if user:
        return JsonResponse({"erro": 1})
    else:
        return JsonResponse({"erro": 0})


# 用户个人中心
def personal_home(request):
    index = request.GET.get('id')
    user = User.objects.filter(staff_number=index)[0]
    txt = {
        'user': user,
    }
    if request.method == 'GET':
        save_action(request, '访问个人中心')
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



# 查看配件
def show_parts(request):
    if request.method == 'GET':
        save_action(request, '查看配件')
        all_parts = Parts.objects.all()
        camera = all_parts.filter(type__device_type='相机')
        sport = all_parts.filter(type__device_type='运动相机')
        UAV = all_parts.filter(type__device_type='无人机')
        switch = all_parts.filter(type__device_type='游戏机')
        num_ls = [len(camera), len(sport), len(UAV), len(switch)]
        data = {}
        data['camera_ls'] = camera.values('parts_type').annotate(Count('parts_type'))
        data['sport_ls'] = sport.values('parts_type').annotate(Count('parts_type'))
        data['UAV_ls'] = UAV.values('parts_type').annotate(Count('parts_type'))
        data['switch_ls'] = switch.values('parts_type').annotate(Count('parts_type'))
        txt = {
            'num_ls': num_ls,
            'total': data,
            'all': all_parts,
        }
        return render(request, 'device_manage/base/parts.html', txt)
    elif request.method == 'POST':
        if request.POST.get('type') == '1':
            flag = request.POST.get('flag')
            txt = ''
            if flag == 'i1':
                camera = Parts.objects.filter(type__device_type='相机')
                txt = {'parts': camera}
            elif flag == 'i2':
                sport = Parts.objects.filter(type__device_type='运动相机')
                txt = {'parts': sport}
            elif flag == 'i3':
                UAV = Parts.objects.filter(type__device_type='无人机')
                txt = {'parts': UAV}
            elif flag == 'i4':
                switch = Parts.objects.filter(type__device_type='游戏机')
                txt = {'parts': switch}
            data = render_to_string('device_manage/parts_inner/show_parts.html', txt)
            return HttpResponse(data)
        elif request.POST.get('type') == '2':
            flag = request.POST.get('flag')
            flag1 = request.POST.get('flag1')
            txt = ''
            if flag == 'i1':
                camera = Parts.objects.filter(type__device_type='相机', parts_type=flag1)
                txt = {'parts': camera}
            elif flag == 'i2':
                sport = Parts.objects.filter(type__device_type='运动相机', parts_type=flag1)
                txt = {'parts': sport}
            elif flag == 'i3':
                UAV = Parts.objects.filter(type__device_type='无人机', parts_type=flag1)
                txt = {'parts': UAV}
            elif flag == 'i4':
                switch = Parts.objects.filter(type__device_type='游戏机', parts_type=flag1)
                txt = {'parts': switch}
            data = render_to_string('device_manage/parts_inner/show_parts.html', txt)
            return HttpResponse(data)


# 关于
def about(request):
    return HttpResponse('待开发')