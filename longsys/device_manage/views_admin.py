from device_manage.views import *


# 管理员用户管理
def user_list(request):
    save_action(request, '进入管理人员界面')
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    user_list = User.objects.all()
    # 记录显示进行分页
    page = request.GET.get('page')
    page_size = 15
    paginator = Paginator(user_list, page_size)
    page_data = paginator.page(page)  # 分好的数据
    txt = {
        'page': page,
        'user_list': page_data,
    }
    return render(request, 'device_manage/admin/user_list.html', txt)


def manage_devices(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    # 获取设备总数
    d_type = DeviceType.objects.all()
    device_ls = [Device.objects.filter(device_type_id=i) for i in [t.id for t in d_type]]  # 对应设备
    sum_ls = [len(i) for i in device_ls]
    total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))  # 分类查询个数
    total_dict = {}
    for d in total_num:
        total_dict[d.get('device_spec')] = d.get('device_spec__count')
    if request.method == 'GET':
        save_action(request, '进入设备管理界面')
        page = int(request.GET.get('page', 1))
        devices = Device.objects.all()
        # 获取下拉框内容
        options = {
            'type': [],
            'spec': [],
            'brand': [],
            'ver': [],
            'card': [],
            'slog': [],
            'state': []
        }
        for d in devices:
            if d.device_type.device_type not in options.get('type'):
                options.get('type').append(d.device_type.device_type)
            if d.device_spec not in options.get('spec'):
                options.get('spec').append(d.device_spec)
            if d.device_brand not in options.get('brand') and d.device_brand is not '':
                options.get('brand').append(d.device_brand)
            if d.device_fw_ver not in options.get('ver') and d.device_fw_ver is not '':
                options.get('ver').append(d.device_fw_ver)
            if d.device_card not in options.get('card') and d.device_card is not '':
                options.get('card').append(d.device_card)
            if d.device_card_slog not in options.get('slog') and d.device_card_slog is not '':
                options.get('slog').append(d.device_card_slog)
            if d.device_state.state not in options.get('state'):
                options.get('state').append(d.device_state.state)
        # 分页
        num_list = [i for i in range(1, len(devices)+1)]
        data_list = [(num_list[i], devices[i], total_dict.get(devices[i].device_spec)) for i in range(len(devices))]
        page_size = 30
        page_nums = int(math.ceil(len(data_list) / page_size))
        page_data = data_list[(page-1) * page_size: page*page_size]
        if page_nums >= 4:
            if page + 4 > page_nums:
                page_num_list = [p for p in range(page_nums - 3, page_nums + 1)]  # 页码列表
            else:
                page_num_list = [p for p in range(page, page + 4)]
        else:
            page_num_list = [p for p in range(1, page_nums + 1)]
        txt = {
            'data_list': page_data,
            'sum': sum_ls,
            'page_nums': page_nums,
            'now_page': page,
            'before_next': [page-1, page+1],
            'page_num_list': page_num_list,
            'options': options,
        }
        return render(request, 'device_manage/admin/manage_devices.html', txt)


@csrf_exempt
def filter_data(request):
    way = request.POST.get('way')
    value = request.POST.get('value')
    devices = Device.objects.all()
    # 取得选项
    options = {
        'type': [],
        'spec': [],
        'brand': [],
        'ver': [],
        'card': [],
        'slog': [],
        'state': []
    }
    for d in devices:
        if d.device_type.device_type not in options.get('type'):
            options.get('type').append(d.device_type.device_type)
        if d.device_spec not in options.get('spec'):
            options.get('spec').append(d.device_spec)
        if d.device_brand not in options.get('brand') and d.device_brand is not '':
            options.get('brand').append(d.device_brand)
        if d.device_fw_ver not in options.get('ver') and d.device_fw_ver is not '':
            options.get('ver').append(d.device_fw_ver)
        if d.device_card not in options.get('card') and d.device_card is not '':
            options.get('card').append(d.device_card)
        if d.device_card_slog not in options.get('slog') and d.device_card_slog is not '':
            options.get('slog').append(d.device_card_slog)
        if d.device_state.state not in options.get('state'):
            options.get('state').append(d.device_state.state)
    # 查询
    total_num = Device.objects.values('device_spec').annotate(Count('device_spec'))  # 分类查询个数
    total_dict = {}
    for d in total_num:
        total_dict[d.get('device_spec')] = d.get('device_spec__count')
    if way == 'type':
        data = devices.filter(device_type__device_type=value)
    elif way == 'spec':
        data = devices.filter(device_spec=value)
    elif way == 'brand':
        data = devices.filter(device_brand=value)
    elif way == 'support':
        data = devices.filter(device_support=value)
    elif way == 'ver':
        data = devices.filter(device_fw_ver=value)
    elif way == 'card':
        data = devices.filter(device_card=value)
    elif way == 'slog':
        data = devices.filter(device_slog=value)
    elif way == 'state':
        data = devices.filter(device_state__state=value)
    else:
        data = 'fail'
    data_list = [(d, total_dict.get(d.device_spec)) for d in data]
    txt = {
        'data_list': data_list,
        'options': options,
    }
    json_data = render_to_string('device_manage/admin/filter_data.html', txt)
    # print(json_data)
    return JsonResponse({'data': json_data}, safe=False)


def device_detail(request):
    d_id = request.GET.get('d_id')
    device = Device.objects.get(id=d_id)
    txt = {
        'device': device,
    }
    return render(request, 'device_manage/base/device_detail.html', txt)


# 新增设备中选择设备改变对应表单
def change_type(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    new_type = request.POST.get('type')
    data = ''
    if new_type == '相机' or new_type == '摄像机' or new_type == '运动相机':
        data = render_to_string('device_manage/add_device/camera.html', {})
    elif new_type == '行车记录仪':
        data = render_to_string('device_manage/add_device/DVR.html', {})
    elif new_type == '监控':
        data = render_to_string('device_manage/add_device/IPC.html', {})
    elif new_type == '无人机':
        data = render_to_string('device_manage/add_device/UAV.html', {})
    elif new_type == '游戏机':
        data = render_to_string('device_manage/add_device/switch.html', {})
    return HttpResponse(data)


# 新增设备
def add_device(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        save_action(request, '访问新增界面')
        device_types = DeviceType.objects.all()
        txt = {
            'type': device_types,
        }
        return render(request, 'device_manage/admin/add_device.html', txt)
    elif request.method == 'POST':
        save_action(request, '新增设备')
        state = State.objects.get(state='可使用')
        dtype = request.POST.get('type', '')
        d_type = DeviceType.objects.get(device_type=dtype)
        d_id = request.POST.get('brand', '')
        brand = request.POST.get('device_id', '')
        spec = request.POST.get('spec', '')
        year = int(request.POST.get('year', ''))
        support = get_value(request.POST.get('support', ''))
        fw = request.POST.get('fw', '')
        CPU = request.POST.get('CPU', '')
        card = request.POST.get('card', '')
        slog = request.POST.get('slog', '')
        if slog == 'single':
            slog = request.POST.getlist('single_slog_choose')
        elif slog == 'double':
            slog = '/'.join(request.POST.getlist('double_slog_choose'))
        card_capacity = request.POST.get('sd-type', '')
        if card_capacity == 'sd':
            card_capacity = '/'.join(request.POST.getlist('SD'))
        elif card_capacity == 'microsd':
            card_capacity = '/'.join(request.POST.getlist('mSD'))
        else:
            card_capacity = 'NA'
        sys = request.POST.get('sys', '')
        i_format = request.POST.get('img_format', '')
        i_avg = get_value(request.POST.get('img_speed', ''))
        v_format = request.POST.get('video_format', '')
        v_speed = get_value(request.POST.get('video_speed', ''))
        v_max = request.POST.get('video_max', '')
        v_cut = request.POST.get('cut_input', '')
        speed = get_value(request.POST.get('speed', ''))
        max_reso = request.POST.get('max_reso', '')
        character = request.POST.get('character', '')
        temper = get_value(request.POST.get('temper', ''))
        vol_ele = get_value(request.POST.get('vol_ele', ''))
        card_vol = get_value(request.POST.get('card_vol', ''))
        p_id = get_value(request.POST.get('pro_id', ''))
        p_belong = get_value(request.POST.get('pro_belong', ''))
        begin = get_value(request.POST.get('begin', ''))
        price = get_value(request.POST.get('price', ''))
        camera_num = request.POST.get('camera_num', 0)
        min_extra = get_value(request.POST.get('min_extra', ''))
        max_extra = get_value(request.POST.get('m_extra', ''))
        extra_capacity = f'{min_extra}—{max_extra}'
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
            per_img, character, state, p_id, begin, p_belong, price,
            extra_capacity,
        )
        self.save()
        return redirect('/manage_devices/')


# EXCEL批量上传
def many_devices(request):
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        save_action(request, '访问上传文件页面')
        types = DeviceType.objects.all()
        txt = {
            'types': types,
        }
        return render(request, 'device_manage/admin/many_devices.html', txt)
    elif request.method == 'POST':
        choosed = request.POST.get('choose_type')
        # Ajax选择类型
        if choosed:
            request.session['choose_type'] = choosed

            return HttpResponse(f'选择【{choosed}】完成,可上传文件')
        # 普通post上传
        else:
            # 保存上传的excel
            file = request.FILES.get('file')
            f_name = ''
            if file:
                f_name = file.name
                f = FileSystemStorage()
                f.save('excel_data/%s' % (f_name), file)
                excel_record = ExcelRecord()
                excel_record.user = User.objects.get(name=name)
                excel_record.filename = f_name
                excel_record.time = datetime.datetime.now()
                excel_record.save()
            # 处理excel
            excel_path = settings.MEDIA_ROOT + f'/excel_data/{file}'
            choosed = request.session.get('choose_type')
            try:
                init_start.many_device(excel_path, choosed)
                return redirect('/many_devices/')
            except:
                return render(request, 'device_manage/samples/error-file.html', {})


def delete_device(request):
    save_action(request, '删除设备')
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    d_id = request.POST.get('device_id')
    d = Device.objects.get(id=d_id)
    d.delete()
    return HttpResponse('OK')


def modify_device(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    d_id = request.GET.get('id')
    device = Device.objects.get(id=d_id)
    if request.method == 'GET':
        device_types = DeviceType.objects.all()
        device_state = State.objects.all()
        extra = device.extra_capacity
        txt = {
            'device': device,
            'type': device_types,
            'state': device_state,
            'min_extra': extra.split('—')[0] if extra else 0,
            'max_extra': extra.split('—')[1] if extra else 0,
        }
        return render(request, 'device_manage/admin/modify_device.html', txt)
    elif request.method == 'POST':
        save_action(request, f'修改设备{d_id}')
        is_problem = request.POST.get('isProblem')
        if is_problem == '0':
            is_problem = False
        else:
            is_problem = True
        device.is_problem = is_problem
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
        device.device_price = request.POST.get('price')
        device.device_camera_num = request.POST.get('camera_num')
        per_img = request.FILES.get('img')
        if per_img:
            f = FileSystemStorage()
            per_img = f.save('img/%s' %(per_img.name), per_img)
            device.device_per_img = per_img
        device.save()
        return redirect('/manage_devices/')


# 查看单个设备记录
def device_record(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        save_action(request, '查看测试记录')
        id = request.GET.get('id')
        record = TestRecord.objects.filter(device_id=id)
        record_ls = []
        for re in record:
            # 查询该条记录所属的需求
            requirements = TestRequirements.objects.filter(id=re.task_id)[0]
            device = Device.objects.filter(id=re.device_id)[0]
            fail_pro = PersonalTask.objects.filter(test_device=re.device_id).filter(task_id=re.task_id)[0].fail_project
            dict = {}
            dict['record'] = re
            dict['device'] = device
            dict['requirements'] = requirements
            dict['fail_pro'] = fail_pro
            record_ls.append(dict)
        txt = {
            'record_ls':record_ls,
        }
        return render(request, 'device_manage/admin/device_record.html', txt)


def reject_demand(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    txt = request.POST.get('txt')
    r_id = request.POST.get('r_id')
    try:
        requirement = TestRequirements.objects.get(id=r_id)
        if requirement.is_finished is not None:
            return HttpResponse('该需求已经开始执行，不能驳回')
        elif PersonalTask.objects.filter(task=requirement).count() != 0:
            return HttpResponse('该需求已经开始执行，不能驳回')
        requirement.is_rejected = True
        requirement.reject_reason = txt
        requirement.rejecter = request.session.get('name')
        requirement.save()
        save_action(request, f'驳回需求{r_id}')
        return HttpResponse('该需求已驳回！')
    except:
        return HttpResponse('fail')


def allot_demand(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    name = request.session.get('name')
    alloter = User.objects.get(name=name)
    r_id = request.GET.get('rid')       # 获取任务号
    require = TestRequirements.objects.get(id=r_id)
    if request.method == 'GET':
        d_id = require.device.split('/')  # 对应device的id
        save_action(request, '分配需求')
        d_ls = []                       # 根据id找到对应device列表
        alloted_num = 0
        tester = User.objects.all()
        allot = AllotTasks.objects.filter(task_id=require)
        for d in d_id:
            username = None
            for a in allot:
                if d in a.test_device[:-1].split('/'):
                    username = a.username
                    break
            device = Device.objects.get(id=d)
            if username:
                d_ls.append([device, username])
                alloted_num += 1
            else:
                d_ls.append([device, None])
        # 整个任务分配情况，若全部分完则由【未分配】变为【进行中】
        if alloted_num == len(d_id):
            require.is_finished = False
            require.save()
        ver = CompatibleVer.objects.values_list('ver', flat=True).distinct()
        txt = {
            'requirements': require,
            'devices': d_ls,
            'tester': tester,
            'r_id': r_id,
            'ver': ver,
        }
        return render(request, 'device_manage/admin/allot_demand.html', txt)
    elif request.method == 'POST':
        allot_method = request.POST.get('allot_type')
        # 1表示接收多个分配数据信息
        if allot_method == '1':
            devices = request.POST.getlist('devices[]')
            tester = request.POST.get('user')
            devices = [Device.objects.get(id=d.split('-')[1]) for d in devices]
            user = User.objects.get(id=tester)
            state_testing = State.objects.get(id=9)
            for d in devices:
                # 写入给个人任务表
                person = PersonalTask()
                person.task = require
                person.test_user = user
                person.test_device = d
                person.save()
                # 写入测试记录表
                new_test = TestRecord()
                new_test.device = d
                new_test.user = user
                new_test.task = require
                new_test.save()
                # 写入任务分配表
                try:
                    allot = AllotTasks.objects.get(username=user.name, task_id=require)
                    allot.test_device = allot.test_device + f'{d.id}/'
                    allot.save()
                except:
                    allot = AllotTasks()
                    allot.task = require
                    allot.user = alloter
                    allot.username = user.name
                    allot.test_device = allot.test_device + f'{d.id}/'
                    allot.save()
                d.device_state = state_testing
                d.save()
            # 给测试员发送邮件
            name = user.name
            to_email = []
            email = user.email
            to_email.append(email)
            send_csy(to_email, name)
            print('邮件发送完成')
            return HttpResponse('OK')
        # 2表示修改分配信息
        elif allot_method == '2':
            device_id, r_id, tester_name = request.POST.getlist('data_ls[]')
            be_allotted = User.objects.get(id=request.POST.get('id'))
            tester = User.objects.get(name=tester_name)
            # 先找出三个表，并判断是否都是没有开始测试的状态，若任意一个开始测试则不能修改
            # 1/个人任务表
            personal = PersonalTask.objects.get(task_id=r_id, test_device_id=device_id, test_user=tester)
            if personal.test_result is not None:
                return HttpResponse('测试正进行中，无法更改')
            # 2/测试记录表
            record = TestRecord.objects.get(task_id=r_id, device_id=device_id, user=tester)
            if record.result is not None:
                return HttpResponse('测试正进行中，无法更改')
            # 3/任务分配表
            allot = AllotTasks.objects.get(task_id=r_id, username=tester_name)
            if allot.is_finish != 0:
                return HttpResponse('测试正进行中，无法更改')
            # 全部通过后方可开始调整
            # 调整个人任务表
            personal.test_user = be_allotted
            personal.save()
            # 调整测试记录表
            record.user = be_allotted
            record.save()
            # 调整任务分配表
            allot_ls = allot.test_device[:-1].split('/')
            if len(allot_ls) == 1:
                allot.delete()
            else:
                allot_ls.remove(device_id)
                allot.test_device = '/'.join(allot_ls) + '/'
                allot.save()
            try:
                be_allotted_data = AllotTasks.objects.get(task_id=r_id, username=be_allotted.name)
                be_allotted_data.test_device = be_allotted_data.test_device + f'{device_id}/'
                be_allotted_data.save()
            except:
                new_allot = AllotTasks()
                new_allot.task = require
                new_allot.user = alloter
                new_allot.username = be_allotted.name
                new_allot.test_device = f'{device_id}/'
                new_allot.save()
            alloted_num = AllotTasks.objects.filter(task=require).count()
            d_id = require.device.split('/')
            if alloted_num == len(d_id):
                require.is_finished = False
            send_csy([be_allotted.email], be_allotted.name)
            return HttpResponse('重新分配完成！通知已发放。')
        # 3表示修改兼容版本
        elif allot_method == '3':
            ver = request.POST.get('ver')
            require.compatible_ver = ver
            require.save()
            return HttpResponse(f'兼容性测试版已修改为：【{ver}】！')


# 管理员查找用户
def search_user(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    name = request.POST.get('data')
    user = User.objects.filter(name=name)
    txt = {
        'user_list': user,
    }
    return render(request,'device_manage/admin/search_user.html', txt)


# 管理员查看用户信息详情或修改用户信息
def user_detail(request, index):
    save_action(request, '管理用户')
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
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
        'group_list': group_list,
        'job_list': job_list,
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


@csrf_exempt
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
            print(types)
            if '问题设备' in types and len(types) > 1:
                devices = []
                for i in types:
                    d = Device.objects.filter(device_type__device_type=i, is_problem=True)
                    for j in d:
                        devices.append([total_dict.get(j.device_spec), j])
            elif '问题设备' in types and len(types) == 1:
                devices = []
                d = Device.objects.filter(is_problem=True)
                for j in d:
                    devices.append([total_dict.get(j.device_spec), j])
            elif len(types) == 0:
                devices = []
                d = Device.objects.all()
                for j in d:
                    devices.append([total_dict.get(j.device_spec), j])
            else:
                devices = []
                for i in types:
                    d = Device.objects.filter(device_type__device_type=i)
                    for j in d:
                        devices.append([total_dict.get(j.device_spec), j])
            txt = {
                'devices': devices,
            }
            data = render_to_string('device_manage/admin/ajax_find_devices.html', txt)
            return HttpResponse(data)
        # 通过编号、型号搜索
        else:
            input_txt = request.POST.get('input')
            devices = []
            device = Device.objects.filter(device_id__contains=input_txt)
            for d in device:
                devices.append([total_dict.get(d.device_spec), d])
            if len(devices) == 0:
                device = Device.objects.filter(device_spec__contains=input_txt)
                for d in device:
                    devices.append([total_dict.get(d.device_spec), d])
            txt = {
                'devices': devices,
                'input': input_txt,
            }
            data = render_to_string('device_manage/admin/ajax_find_devices.html', txt)
            return HttpResponse(data)


# 局部刷新测试记录排序
def card_num_sort(request):
    if request.method == 'POST':
        types = request.POST.get('types')
        history_list = []
        if types == '3':
            name = request.POST.get('name')
            try:
                user = User.objects.filter(name=name)[0]
                test_history = TestRequirements.objects.filter(is_finished__isnull=False).filter(initiator=user)
            except:
                test_history = []
        else:
            test_history = TestRequirements.objects.filter(is_finished__isnull=False).order_by('-id')
        for h in test_history:
            h_id = h.id
            p_task = PersonalTask.objects.filter(task_id=h_id)
            # 已完成
            is_finish = len(p_task.filter(test_result__isnull=False))
            # 总数
            all = len(p_task)
            start_time = h.start_time
            end_time = h.end_time
            initiator = h.initiator
            history_list.append(
                [h_id,is_finish,all,start_time,end_time,initiator]
            )
        txt = {
            'history_ls':history_list,
        }
        data = render_to_string('device_manage/base/test_history_sort.html', txt)
        return HttpResponse(data)


def add_parts(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        parts_type = Parts.objects.values('parts_type').distinct()
        device_types = DeviceType.objects.all()
        txt = {
            'type': device_types,
            'parts_type': parts_type,
        }
        return render(request, 'device_manage/admin/add_parts.html', txt)
    elif request.method == 'POST':
        d_type = request.POST.get('d-type')
        brand = request.POST.get('brand', '')
        p_type = request.POST.get('type', '')
        code = request.POST.get('code', '')
        num = request.POST.get('num', '')
        new_parts = Parts()
        new_parts.type = DeviceType.objects.get(device_type=d_type)
        new_parts.brand = brand
        new_parts.p_type = p_type
        new_parts.code = code
        new_parts.num = num
        new_parts.save()
        save_action(request, '新增配件')
        return redirect('/parts/')


def modify_parts(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        p_id = request.GET.get('id')
        this_part = Parts.objects.get(id=p_id)
        device_types = DeviceType.objects.all()
        request.session['parts_id'] = p_id
        parts_type = Parts.objects.values('parts_type').distinct()
        txt = {
            'type': device_types,
            'part': this_part,
            'id': p_id,
            'parts_type': parts_type,
        }
        return render(request, 'device_manage/admin/modify_parts.html', txt)
    else:
        p_id = request.session.get('parts_id')
        new_parts = Parts.objects.get(id=p_id)
        d_type = request.POST.get('d-type')
        brand = request.POST.get('brand', '')
        p_type = request.POST.get('type', '')
        code = request.POST.get('code', '')
        num = request.POST.get('num', '')
        new_parts.type = DeviceType.objects.get(device_type=d_type)
        new_parts.brand = brand
        new_parts.p_type = p_type
        new_parts.code = code
        new_parts.num = num
        new_parts.save()
        save_action(request, '修改配件')
        return redirect('/parts/')


# 分配需求列表
def manage_demand(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        save_action(request, '访问管理需求界面')
        requirements = TestRequirements.objects.filter(is_rejected=False).order_by('is_finished')
        rej_requirements = TestRequirements.objects.filter(is_rejected=True)
        demand = []
        rejected = []
        for r in requirements:
            demand.append([len(r.device.split('/')), r])
        for r in rej_requirements:
            rejected.append([len(r.device.split('/')), r])
        txt = {
            'demand': demand,
            'rej_demand': rejected,
        }
        return render(request, 'device_manage/admin/manage_demand.html', txt)


# 下载测试记录
def export_record(request, index):
    save_action(request, '下载测试记录')
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    if is_admin:
        history = TestRecord.objects.filter(task_id=index)
    else:
        user_id = User.objects.filter(name=name)[0]
        history = TestRecord.objects.filter(task_id=index).filter(user_id=user_id)
    history_ls = []
    for h in history:
        dict = {}
        dict['task'] = h
        dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
        dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
        history_ls.append(dict)
    # 需求表数据：测试版本，搭配等
    requirements = TestRequirements.objects.filter(id=index)[0]
    dev_num = len(requirements.device.split('/'))  # 平台总数
    fail_num = len(history.filter(result=0))  # 失败平台数
    if request.method == 'GET':
        check_ls = request.session.get('check_ls')
        txt = {
            'history': history_ls,
            'requirements': requirements,
            'dev_num': dev_num,
            'fail_num': fail_num,
            'check_ls': check_ls,
        }
        return render(request, 'device_manage/admin/check_record.html', txt)
    elif request.method == 'POST':
        # 按勾选框刷新显示记录
        check_ls = request.POST.get('check_ls')
        if check_ls == '[]':    # 加入未勾选则默认为全部
            check_ls = ['card_num', 'test_cycle', 'compatible_ver', 'device_support', 'device_card_slog', 'card_num_1',
                        'card_id', 'user', 'remark', 'fail_pro']
        else:
            check_ls = check_ls[1:-1].replace('"', '').split(',')
        request.session['check_ls'] = check_ls
        return JsonResponse({'msg': '正在导出'})


# 筛选测试记录
def choose_result(request, index):
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    result = request.POST.get('sel')
    flag = request.POST.get('flag')
    history_ls = []
    device_type = []
    device_brand = []
    device_spec = []
    card_slog = []
    staff_ls = []
    ver = ''
    ver_step1 = ''
    if is_admin:
        history = TestRecord.objects.filter(task_id=index)
    else:
        user_id = User.objects.filter(name=name)[0]
        history = TestRecord.objects.filter(task_id=index).filter(user_id=user_id)
    for item in history:
        # 查询整个需求中涉及的设备类型
        device_t = item.device.device_type.device_type
        if device_t not in device_type:
            device_type.append(device_t)
        # 查询整个需求中涉及的设备品牌
        device_b = item.device.device_brand
        if device_b not in device_brand:
            device_brand.append(device_b)
        # 查询整个需求中涉及的设备型号
        device_s = item.device.device_spec
        if device_s not in device_spec:
            device_spec.append(device_s)
        # 查询整个需求中涉及的设备卡槽
        card_s = item.device.device_card_slog
        if card_s not in card_slog:
            card_slog.append(card_s)
        # 查询整个需求中涉及的测试人员
        staff = item.user.name
        if staff not in staff_ls:
            staff_ls.append(staff)
        # 查询整个需求的兼容性测试版本
        ver = item.task.compatible_ver
        if ver == 'CV1.0.0':
            ver_step1 = CV100.objects.all()
        elif ver == 'CV1.1.0':
            ver_step1 = CV110.objects.all()
        elif ver == 'DV1.0.0':
            ver_step1 = DV100.objects.all()
        elif ver == 'IV1.0.0':
            ver_step1 = IV100.objects.all()
        elif ver == 'RV1.0.0':
            ver_step1 = RV100.objects.all()
        elif ver == 'MV1.0.0':
            ver_step1 = MV100.objects.all()
        elif ver == 'DrV1.0.0':
            ver_step1 = DrV100.objects.all()
    if flag == 'result':
        if result == ' ':
            for h in history:
                if h.result == None:
                    dict = {}
                    dict['task'] = h
                    dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                    dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                    dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[
                        0].fail_step
                    history_ls.append(dict)
        else:
            for h in history:
                if h.result == int(result):
                    dict = {}
                    dict['task'] = h
                    dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                    dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                    dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[
                        0].fail_step
                    history_ls.append(dict)
    elif flag == 'device_type':
        for h in history:
            if h.device.device_type.device_type == result:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'device_brand':
        for h in history:
            if h.device.device_brand == result:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'device_spec':
        for h in history:
            if h.device.device_spec == result:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'support':
        for h in history:
            if h.device.device_support == int(result):
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'card_slog':
        for h in history:
            if h.device.device_card_slog == result:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'staff':
        for h in history:
            if h.user.name == result:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    elif flag == 'f_pro':
        for h in history:
            p_task = PersonalTask.objects.filter(task_id=h.task_id).filter(test_device=h.device_id)[0]
            if result in p_task.fail_project:
                dict = {}
                dict['task'] = h
                dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
                dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
                dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
                history_ls.append(dict)
    txt = {
        'history': history_ls,
        'index': index,
        'device_type': device_type,
        'device_brand': device_brand,
        'device_spec': device_spec,
        'card_slog': card_slog,
        'staff_ls': staff_ls,
        'fail_ls': ver_step1,
        'compatible_ver': ver,
        'ver_step': ver_step1,
    }
    return render(request, 'device_manage/admin/choose_result.html', txt)


# 查看测试记录
def test_history(request):
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    master_control = Collocation.objects.filter(category=0)
    flash = Collocation.objects.filter(category=1)
    # flash简称有相同的,去重显示
    flash_ls = list(set([ f.abbreviation for f in flash ]))
    die = Collocation.objects.filter(category=2)
    honeycomb = Collocation.objects.filter(category=3)
    capacity = Collocation.objects.filter(category=4)
    if request.method == 'GET':
        save_action(request, '查看测试记录')
        data_ls = []            # [设备总数, 设备对象, 测完设备数]
        match_ls = []           # 用来存所有的测试搭配
        if is_admin:
            task = TestRequirements.objects.filter(is_finished__isnull=False).order_by('-id')
            for t in task:
                match_ls.append(t.match)
                finished_num = PersonalTask.objects.filter(Q(task=t), Q(test_result__isnull=False))
                data_ls.append([len(t.device.split('/')), t, len(finished_num)])
        else:
            task = AllotTasks.objects.filter(username=name).order_by('-id')
            for t in task:
                req = TestRequirements.objects.filter(id=t.task_id)[0]
                match_ls.append(req.match)
                data_ls.append([len(t.test_device.split('/'))-1, t,req.match])
        # 记录显示进行分页
        page = request.GET.get('page')
        page_size = 15
        paginator = Paginator(data_ls, page_size)
        page_data = paginator.page(page)  # 分好的数据
        txt = {
            'page': page,
            'task': page_data,
            'match_ls':match_ls,
            'master_control':master_control,
            'flash':flash_ls,
            'die':die,
            'honeycomb':honeycomb,
            'capacity':capacity,
        }
        return render(request, 'device_manage/admin/test_history.html', txt)


def choose_match(request):
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    if request.method == 'POST':
        key_match = request.POST.get('match')
        match_ls = []           # 用来存所有的测试搭配
        data_ls = []            # [设备总数, 设备对象, 测完设备数]
        if is_admin:
            task = TestRequirements.objects.filter(is_finished__isnull=False).order_by('-id')
            for t in task:
                match_ls.append(t.match)
                finished_num = PersonalTask.objects.filter(Q(task=t), Q(test_result__isnull=False))
                if t.match == key_match:
                    data_ls.append([len(t.device.split('/')), t, len(finished_num)])
        else:
            task = AllotTasks.objects.filter(username=name).order_by('-id')
            for t in task:
                req = TestRequirements.objects.filter(id=t.task_id)[0]
                match_ls.append(req.match)
                if req.match == key_match:
                    data_ls.append([len(t.test_device.split('/'))-1, t,req.match])
        txt = {
            'task': data_ls,
            'match_ls': match_ls,
        }
        return render(request, 'device_manage/admin/choose_match.html', txt)


# 测试记录详情
def history_detail(request, index,page):
    is_admin = request.session.get('is_admin')
    name = request.session.get('name')
    if request.method == 'GET':
        if is_admin:
            history = TestRecord.objects.filter(task_id=index)
        else:
            user = User.objects.filter(name=name)[0]
            history = TestRecord.objects.filter(task_id=index).filter(user_id=user.id)
        history_ls = []
        device_type = []
        device_brand = []
        device_spec = []
        card_slog = []
        staff_ls = []
        ver = ''
        ver_step1 = ''
        for h in history:
            dict = {}
            dict['task'] = h
            dict['fail_pro'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_project
            dict['remark'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].record
            dict['fail_step'] = PersonalTask.objects.filter(test_device=h.device).filter(task_id=index)[0].fail_step
            history_ls.append(dict)
            # 查询整个需求中涉及的设备类型
            device_t = h.device.device_type.device_type
            if device_t not in device_type:
                device_type.append(device_t)
            # 查询整个需求中涉及的设备品牌
            device_b = h.device.device_brand
            if device_b not in device_brand:
                device_brand.append(device_b)
            # 查询整个需求中涉及的设备型号
            device_s = h.device.device_spec
            if device_s not in device_spec:
                device_spec.append(device_s)
            # 查询整个需求中涉及的设备卡槽
            card_s = h.device.device_card_slog
            if card_s not in card_slog:
                card_slog.append(card_s)
            # 查询整个需求中涉及的测试人员
            staff = h.user.name
            if staff not in staff_ls:
                staff_ls.append(staff)
            # 查询整个需求的兼容性测试版本
            ver = h.task.compatible_ver
        # 需求表数据：测试版本，搭配等
        requirements = TestRequirements.objects.filter(id=index)[0]
        dev_num = len(requirements.device.split('/'))   # 平台总数
        fail_num = len(history.filter(result=0))        # 失败平台数
        # 搭配
        sample_info_list = constants.SAMPLE_INFO_LIST
        master_control = Collocation.objects.filter(category=0)
        flash = Collocation.objects.filter(category=1)
        die = Collocation.objects.filter(category=2)
        honeycomb = Collocation.objects.filter(category=3)
        capacity = Collocation.objects.filter(category=4)
        c_ver = CompatibleVer.objects.values_list('ver', flat=True).distinct()
        step = CompatibleVer.objects.filter(ver=ver)[0].step.split('/')
        test_project = []  # 测试项目列表
        test_step = []  # 测试步骤列表
        # 将测试项目和测试步骤分开
        for item in step:
            if '*' in item:
                pro = item.split('*')[0]
                test_project.append(pro)
                for i in range(1, int(item.split('*')[1]) + 1):
                    if i == 1:
                        s = pro
                    else:
                        s = pro + str(i)
                    test_step.append(s)
            else:
                test_project.append(item)
                test_step.append(item)
        cnt_ls = [x for x in range(1, 11)]  # 记录步骤的重复次数
        # 分页
        page_size = 40
        paginator = Paginator(history_ls, page_size)
        page_data = paginator.page(page)  # 分好的数据
        txt = {
            'history': page_data,
            'requirements': requirements,
            'dev_num': dev_num,
            'fail_num': fail_num,
            'device_type': device_type,
            'device_brand': device_brand,
            'device_spec': device_spec,
            'card_slog': card_slog,
            'staff_ls': staff_ls,
            'fail_ls': test_project,
            'compatible_ver': ver,
            'ver_step': test_step,
            'len_step': len(test_step)-1,
            'sample_info_list': sample_info_list,
            'master_control': master_control,
            'flash': flash,
            'die': die,
            'honeycomb': honeycomb,
            'capacity': capacity,
            'ver': c_ver,
            'index': index,
            'cnt_ls': cnt_ls,
        }
        return render(request, 'device_manage/admin/history_detail.html', txt)
