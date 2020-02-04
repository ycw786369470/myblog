from device_manage.views import *


# 个人测试任务
def personal_task(request):
    name = request.session.get('name')
    if request.method == 'GET':
        save_action(request, '查看个人任务')
        # 查询到分配给自己的所有任务
        task = AllotTasks.objects.filter(username=name).order_by('is_finish')
        task_list = []
        now = datetime.datetime.now()
        for td in task:
            dict = {}
            dict['task'] = td.task
            # 查询任务分配表
            dict['allot'] = td
            dict['num'] = len(td.test_device[:-1].split('/')) if td.test_device != '/' else 0
            task_list.append(dict)
        txt = {
            'task_ls': task_list,
            'now': now,
        }
        return render(request, 'device_manage/tester/personal_task.html', txt)


# 任务详情
def task_detail(request):
    name = request.session.get('name')
    task_id = request.GET.get('id')
    save_action(request, f'查看{task_id}号任务')
    user = User.objects.filter(name=name)
    p_task = PersonalTask.objects.filter(task_id=task_id).filter(test_user=user)
    task_ls = []
    for t in p_task:
        dev = t.test_device
        test_record = TestRecord.objects.filter(task_id=task_id).filter(device=dev)[0]
        task_ls.append([t, test_record])
    requirements = TestRequirements.objects.filter(id=task_id)[0]
    # 兼容性测试版本
    ver = requirements.compatible_ver
    ver_step1 = ''
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
    txt = {
        'requirements':requirements,
        'task_ls': task_ls,
        'length': len(p_task),
        'task_id': task_id,
        'ver_step1':ver_step1,
    }
    return render(request, 'device_manage/tester/task_detail.html', txt)


# 记录结果
def record_result(request):
    is_admin = request.session.get('is_admin')
    if is_admin is None:
        return render(request, 'device_manage/samples/error-403.html')
    staff_number = request.session.get('staff_number')
    if request.method == "POST":
        result = request.POST.get('result')
        id = request.POST.get('id')
        task = PersonalTask.objects.filter(id=id)[0]
        if result == '1':
            re = 1
            task.test_result = re
            task.fail_project = ''
            task.fail_step = ''
            # 取消在设备表中问题设备的标记
            device = Device.objects.filter(id=task.test_device_id)[0]
            device.is_problem = 0
            device.save()
        elif result == '0':
            re = 0
            task.test_result = re
            task.fail_project = request.POST.get('fail')
            task.fail_step = request.POST.get('fail_step')
            # 在设备表中标记为问题设备
            device = Device.objects.filter(id=task.test_device_id)[0]
            device.is_problem = 1
            device.save()
        else:
            re = None
            task.test_result = re
            task.fail_project = ''
            task.fail_step = ''
        task.save()
        # 将数据写到测试记录表中
        # 1.判断记录表中是否存在该设备的测试记录
        device_record = TestRecord.objects.filter(device_id=task.test_device_id).filter(task_id=task.task_id)
        if len(device_record) == 0:
            t = TestRecord()
            # 从需求表中提取相应的总需求
            task_req = TestRequirements.objects.filter(id=task.task_id)[0]
            t.user = User.objects.filter(staff_number=staff_number)[0]
            t.device = task.test_device
            t.task_id = task.task_id
            t.version = task_req.ver
            t.compatible_ver = task_req.ver
            t.result = re
            t.record = task.record
            t.save()
        else:
            device_record = device_record[0]
            device_record.result = re
            device_record.record = task.record
            device_record.save()
        return JsonResponse({'msg': 'true'})


# 提交任务
def check_finish(request):
    if request.method == "POST":
        name = request.session.get('name')
        task_id = request.POST.get('id')
        user = User.objects.get(name=name)
        if request.POST.get('flag') == '0':
            # 校验是否全部测完
            p_task = PersonalTask.objects.filter(task_id=task_id).filter(test_user=user)
            finish_ls = p_task.filter(test_result=None)
            return JsonResponse({'msg': len(finish_ls)})
        elif request.POST.get('flag') == '1':
            # 确认提交
            task = AllotTasks.objects.filter(username=name).filter(task_id=task_id)[0]
            task.is_finish = 1
            task.save()
            # 检查整个任务是否完成
            check_all_task = AllotTasks.objects.filter(task_id=task_id)
            finished = 0
            for t in check_all_task:
                if t.is_finish is False:
                    break
                elif t.is_finish is True:
                    finished += 1
            if finished == len(check_all_task):
                requirement = TestRequirements.objects.get(id=task_id)
                requirement.is_finished = True
                requirement.finish_time = datetime.datetime.now()
                requirement.save()
            save_action(request, f'提交{task_id}任务')
            return JsonResponse({'msg': '提交完成！'})
        elif request.POST.get('flag') == 'r1':
            # 记录
            p_id = request.POST.get('p_id')
            rec = request.POST.get('rec')
            p_task = PersonalTask.objects.filter(task_id=task_id).filter(test_user=user)
            task = p_task.filter(id=p_id)[0]
            task.record = rec
            task.save()
            return JsonResponse({'msg': 'success'})
        elif request.POST.get('flag') == 'card_id':
            p_id = request.POST.get('p_id')
            card_id = request.POST.get('c_id')
            dev = PersonalTask.objects.filter(id=p_id).filter(task_id=task_id)[0].test_device
            # 在记录表中找到该任务中该条设备的记录
            t_record = TestRecord.objects.filter(task_id=task_id).filter(device=dev)[0]
            t_record.card_id = card_id
            t_record.save()
