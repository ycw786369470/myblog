from device_manage.views import *


# 修改搭配，兼容性测试版本等
def reset_match(request):
    if request.method == 'POST':
        # 需求id
        task_id = request.POST.get('id')
        requirements = TestRequirements.objects.filter(id=task_id)[0]
        if request.POST.get('flag') == 'match':
            match = request.POST.get('match')
            SN = request.POST.get('SN')
            requirements.match = match
            requirements.SN = SN + requirements.ver
            requirements.save()
            return JsonResponse({'msg': requirements.SN})
        elif request.POST.get('flag') == 'ver':
            ver = request.POST.get('ver')
            requirements.compatible_ver = ver
            requirements.save()
            return JsonResponse({'msg': 1})


# 修改版本
def reset_ver(request):
    task_id = request.POST.get('id')
    requirements = TestRequirements.objects.filter(id=task_id)[0]
    old_ver = requirements.ver
    new_ver = request.POST.get('t_ver')
    requirements.ver = new_ver
    requirements.SN = requirements.SN.replace(old_ver,new_ver)
    requirements.save()
    return JsonResponse({'msg': requirements.SN})


def new_demand(request):
    is_init = request.session.get('is_init')
    if is_init is None:
        return render(request, 'device_manage/samples/error-403.html')
    if request.method == 'GET':
        save_action(request, '发起需求')
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
        }
        return render(request, 'device_manage/demander/demand_type.html', txt)


def sample_info(request):
    """ 样品信息 """
    start_time = datetime.datetime.now()
    if request.method == 'GET':
        demand_id = request.GET.get('id', 'none')
        request.session['demand_id'] = demand_id
        demand_list = []
        if demand_id != 'none':
            demand = TestRequirements.objects.get(pk=demand_id)
            demand_list.append(demand)
            SN = (demand.match).split('-')
            if len(SN)>4:
                SN[1] = request.session.get('#slt2', None)
                SN.pop(2)
            for i in SN:
                if i == SN[-1]:
                    demand_list.append(Collocation.objects.get(abbreviation=i))
                elif i == SN[1]:
                    demand_list.append(Collocation.objects.get(num=i))
                else:
                    result = Collocation.objects.get(collocation= i)
                    demand_list.append(result)
            demand_list.append(demand_list[0].ver)
            demand_list.append(demand_list[0].P_N)
            demand_list.append(demand_list[0].sample_quantity)
            demand_list.append(demand_list[0].compatible_ver)
        print(demand_list)
        sample_info_list = constants.SAMPLE_INFO_LIST
        master_control = Collocation.objects.filter(category=0)
        flash = Collocation.objects.filter(category=1)
        die = Collocation.objects.filter(category=2)
        honeycomb = Collocation.objects.filter(category=3)
        capacity = Collocation.objects.filter(category=4)
        ver = CompatibleVer.objects.values_list('ver', flat=True).distinct()
        data = {
            'start_time': start_time,
            'sample_info_list': sample_info_list,
            'master_control': master_control,
            'flash': flash,
            'die': die,
            'honeycomb': honeycomb,
            'capacity': capacity,
            'demand_list': demand_list,
            'demand_id': demand_id,
            'ver': ver,
        }
        return render(request, 'device_manage/demander/sample_info.html', data)


def release_task(request):
    """ 发布需求 """
    def func(email_url):
        """
        线程run方法
        :param email_url: 邮件地址
        :return: none
        """
        to_email = []
        name = json.loads(data['info_data'])['name']
        now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        to_email.append(email_url)
        send_admin(to_email, name, now)
    if request.method == 'GET':
        pks = json.loads(request.GET.get('pk'))
        str_pk = ''
        for pk in pks:
            if pk == pks[-1]:
                str_pk = str_pk + str(pk)
            else:
                str_pk = str_pk + str(pk) + ','
        ls = '/'.join(str_pk.split(','))
        file_path = request.session.get('path')
        new_requirement = TestRequirements()
        data = request.session.get('data')
        info_data = json.loads(data.get('info_data'))
        slt_num = json.loads(data.get('slt_num'))
        ver = info_data.get('d2')
        request.session['#slt2'] = slt_num.get('#slt2')
        #  解析搭配,形成唯一的SN
        S_N = slt_num.get('#slt1') + ''\
              + slt_num.get('#slt2') + '' \
              + slt_num.get('#slt3') + ''\
              + slt_num.get('#slt5')
        S_N = S_N + '' + ver
        new_requirement.match = info_data.get('match')
        init = info_data.get('name')
        new_requirement.ver = ver
        new_requirement.P_N = info_data.get('d4')
        new_requirement.SN = S_N
        new_requirement.sample_quantity = info_data.get('d5')
        new_requirement.start_time = info_data.get('start_time')
        new_requirement.end_time = info_data.get('end_time')
        new_requirement.remark = info_data.get('txt', '')
        new_requirement.compatible_ver = info_data.get('slt6', '')
        new_requirement.device = ls
        new_requirement.init_time = datetime.datetime.now()
        new_requirement.initiator = User.objects.get(name=init)
        new_requirement.file_path = file_path
        if request.session['demand_id'] != 'none':
            new_requirement.is_rejected = False
            new_requirement.pk = request.session['demand_id']
        new_requirement.save()
        # 给管理员发送邮件
        admin_ls = User.objects.filter(is_admin=1)
        for ad in admin_ls:
            email_url = ad.email
            t = Thread(target=func, args=(email_url,))
            t.start()
        return redirect('/')
    else:
        data = request.POST.dict()
        info_data = json.loads(data.get('info_data'))
        # 临时存储时间
        request.session['start_time'] = info_data.get('start_time')
        request.session['end_time'] = info_data.get('end_time')
        request.session['data'] = data
        return HttpResponse(1)


def demand_recoder(request):
    save_action(request, '查看发起需求记录')
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    name = request.session.get('name')
    demands = TestRequirements.objects.filter(initiator__name=name, is_rejected=False).order_by('is_finished')
    reject_demands = TestRequirements.objects.filter(initiator__name=name, is_rejected=True)
    total_ls = []
    for d in demands:
        tasks = PersonalTask.objects.filter(task=d)
        total_num = len(tasks)
        finish_num = len(tasks.filter(test_result__isnull=False))
        if d.is_rejected is True:
            state = '被驳回'
        elif d.is_finished is None:
            state = '待分配'
        elif d.is_finished is False:
            state = '测试中'
        elif d.is_finished is True:
            state = '已完成'
        else:
            state = '其他'
        total_ls.append([d, state, total_num, finish_num])
    txt = {
        'total': total_ls,
        'reject': reject_demands,
    }
    return render(request, 'device_manage/demander/demand_recoder.html', txt)


def demand_recoder_detail(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    pk = request.GET.get('id')
    demand = TestRequirements.objects.get(pk=pk)
    demand_num = len(demand.device.split('/')) if len(demand.device) != 0 else 0
    ver = demand.compatible_ver                             # 获取兼容行测试版本
    fail_devices = []
    fail_data = []
    distributor = {}
    tester_record = []                                      # 测试员的完成度
    tasks = AllotTasks.objects.filter(task=demand)          # 该需求的分配表
    records = TestRecord.objects.filter(task=demand)        # 该需求的所有任务记录
    pass_num = len(records.filter(result=1))
    fail_num = len(records.filter(result=0))
    finish_num = len(records.filter(result__isnull=False))
    count = len(records)
    pass_ratio = []
    if demand.is_rejected is True:
        state = '被驳回'
    elif demand.is_finished is None:
        state = '待分配'
    elif demand.is_finished is False:
        state = '测试中'
        find_tasks = tasks.filter(task=demand)
        user = find_tasks[0].user if len(find_tasks) != 0 else '历史测试'
        distributor['user'] = user                                                      # 获取该需求分配人姓名
        distributor['tester'] = [d.get('username') for d in tasks.values('username')]   # 获取该需求所有测试员姓名
        for uname in distributor['tester']:
            person_finish = len(records.filter(user__name=uname, result__isnull=False))
            person_all = len(records.filter(user__name=uname))                          # 个人任务总数
            ratio = int((person_finish / person_all)*100)
            tester_record.append([uname, person_finish, person_all, ratio])
    elif demand.is_finished is True:
        state = '已完成'
        find_tasks = tasks.filter(task=demand)
        user = find_tasks[0].user if len(find_tasks) != 0 else '历史测试'
        distributor['user'] = user
        distributor['tester'] = [d.get('username') for d in tasks.values('username')]
        fail_devices = PersonalTask.objects.filter(task=demand, test_result=False)
        fail_data = fail_devices.values('fail_project').annotate(Count('fail_project'))
        errors_num = 0      # 记录错误总数，生成百分比
        for f in fail_data:
            errors_num += f.get('fail_project__count')
        for f in fail_data:
            f['percent'] = int((f.get('fail_project__count') / errors_num) * 100)
        pass_ratio = int((pass_num / count) * 100)
    else:
        state = '其他'
    admins = User.objects.filter(is_admin=True)
    txt = {
        'demand': demand,
        'demand_num': demand_num,
        'state': state,
        'finished': finish_num,
        'total_num': count,
        'distributor': distributor,
        'pass': pass_num,
        'fail': fail_num,
        'record': tester_record,
        'c_ver': ver,
        'fail_device': fail_devices,
        'fail_data': fail_data,
        'pass_ratio': pass_ratio,
        'admins': admins,
    }
    return render(request, 'device_manage/demander/demand_recoder_detail.html', txt)


class New_built(New_Built_View):
    """ 设备待选与需求发布  """
    # 模板位置
    template_name = '../templates/device_manage/demander/new_built.html'

    def get_queryset(self):
        """ 获取数据集 """
        #  上传fw包
        if self.request.method == "POST":
            file = self.request.FILES.get('zip')
            if file:
                file_path = os.path.join(settings.MEDIA_ROOT, 'media\\' + file.name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    f = FileSystemStorage()
                    path = f.save('media/%s' % file.name + '', file)
                    self.request.session['path'] = path.split('/')[1]
                else:
                    f = FileSystemStorage()
                    path = f.save('media/%s' % file.name + '', file)
                    self.request.session['path'] = path.split('/')[1]
        # 后端更新种类与品牌时前台也能同步更新
        category = {}
        category_obj = DeviceType.objects.all()
        # new_demand 列名
        demand_list = constants.DEMAND_LIST
        # new_built 列名
        column_names = constants.DEVICE_SHOW_COLUMN_NAMES
        if len(category_obj):
            for item in category_obj:
                category_id = item.pk
                devices = Device.objects.filter(device_type_id=category_id)
                brand = set()
                for device in devices:
                    brand.add(device.device_brand)
                # 该类型的品牌
                brand = list(brand)
                category[item.device_type] = brand
        else:
            return None

        # 获取年份
        years = Device.objects.values_list('device_year', flat=True)
        years = sorted(list(set(years)))
        # 获取卡型
        card = Device.objects.values_list('device_card', flat=True)
        card = list(set(card))
        for i in card:
            if i is None:
                card.remove(i)
        # 获取卡槽
        card_slog = Device.objects.values_list('device_card_slog', flat=True)
        card_slog = list(set(card_slog))
        for i in card_slog:
            if i is None:
                card_slog.remove(i)
        # 处理复选框中和搜索框的内容
        search_data = self.request.GET.dict()
        queryset = Device.objects.all()
        if search_data:
            List_check = search_data.get('list')
            device_id = search_data.get('device')
            if List_check:
                data = json.loads(List_check)
                for k, v in data.items():
                    if k == 'selected_txt1':
                        queryset = queryset.filter(device_type_id=v)
                    elif k == 'selected_txt2':
                        queryset = queryset.filter(device_brand=v)
                    elif k == 'selected_txt3':
                        queryset = queryset.filter(device_support=v)
                    elif k == 'selected_txt4':
                        queryset = queryset.filter(device_year=int(v))
                    elif k == 'selected_txt5':
                        if v == '0':
                            queryset = queryset.order_by('device_id')
                        elif v == '1':
                            queryset = queryset.order_by('device_year')
                    elif k == 'selected_txt6':
                        queryset = queryset.filter(device_card_slog=v)
                    elif k == 'selected_txt7':
                        queryset = queryset.filter(device_card=v)
                    elif k == 'selected_txt8':
                        queryset = queryset.filter(is_problem=True)
            elif device_id:
                query = Q(device_id__icontains=device_id)
                query = query | Q(device_spec__icontains=device_id)
                queryset = queryset.filter(query)
        # 全选/单选
        select_list = self.request.GET.getlist('select_list[]')
        select_list = [int(i) for i in select_list]
        select_list = list(set(select_list))
        select_queryset = []
        if select_list:
            for i in select_list:
                result = queryset.filter(pk=int(i))
                if result:
                    select_queryset.append(result[0])
        # 获取时间
        start_time = self.request.session.get('start_time')
        end_time = self.request.session.get('end_time')

        return {
            'category': category,
            'column_names': column_names,
            'queryset': queryset,
            'select_queryset': select_queryset,
            'select_list': select_list,
            'years': years,
            'demand_list': demand_list,
            'start_time': start_time,
            'end_time': end_time,
            'card': card,
            'card_slog': card_slog,
        }

    def get_context_data(self, **kwargs):
        " 添加额外的参数 """
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.request.GET.dict()

        return context


class Device_search(ListView):
    """" 设备列表 """
    # 每页放多少条数据
    paginate_by = constants.SEARCH_PAGE_SIZE
    # 模板位置
    template_name = 'device_manage/base/device_search.html'

    def get_queryset(self):
        # 判断session中的身份
        identity = self.request.session.get('name')
        # 按名称搜索
        name = self.request.GET.get('name', '')
        Queryset = Device.objects.all()
        query = Q(device_brand__icontains=name) | \
                Q(device_support__icontains=name) | \
                Q(device_begin__icontains=name) | \
                Q(device_card__icontains=name) | \
                Q(device_spec__icontains=name.upper()) | \
                Q(device_year__icontains=name)
        Queryset = Queryset.filter(query)
        return Queryset

    def get_context_data(self, **kwargs):
        """ 添加额外的参数, 添加搜索参数 """
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.request.GET.dict()
        return context