# 该文件用来新建数据信息，转移至新的计算机启动前调用添加基本信息
from django.shortcuts import redirect, HttpResponse
from device_manage.models import *
import xlrd
import os
import datetime


def new_tpye(request):
    d = [
        {'device': '相机', 'intro': 'SD/TF'},
        {'device': '摄像机', 'intro': 'SD/TF'},
        {'device': 'Surface', 'intro': 'SD'},
        {'device': '手机', 'intro': 'TF'},
        {'device': '行车记录仪', 'intro': 'TF'},
        {'device': '监控', 'intro': 'TF'},
        {'device': '无人机', 'intro': 'TF'},
        {'device': '运动相机', 'intro': 'TF'},
        {'device': '游戏机', 'intro': 'TF'},
        {'device': '智能门铃', 'intro': 'TF'},
    ]
    ret = DeviceType.objects.all()
    if len(ret) == 0:
        d_type = DeviceType()
        for i in d:
            new = d_type.add_type(i.get('device'), i.get('intro'))
            new.save()
    # return redirect('/')


def new_state(request):
    d = ['可使用', '维护中', '无电池', '卡槽损坏', '借出', '租赁', '其他', '无充电器', '测试中']
    for i in d:
        new = State()
        new.state = i
        new.save()
    # return redirect('/')


def new_job(request):
    d = ['实习生', '测试员', '测试主管', '助理测试工程师', '测试技工', '测试工程师', '其他']
    for i in d:
        new = Job()
        new.job_name = i
        new.save()
    # return redirect('/')


def new_group(request):
    d = ['嵌入式', 'SSD', '移动存储', '微存储', '其他']
    for i in d:
        new = Group()
        new.group_name = i
        new.save()
    # return redirect('/')


def new_device(request):
    d = [{'d_type': '相机', 'd_id': 'C030-03ab-1', 'brand': 'Canon', 'spec': '760D', 'year': 2013,
          'num': 1, 'support': 0, 'fw': 'Ver.1.1.1', 'CPU': 'i7', 'card': 'SD/SDHC/SDXC',
          'slog': 'UHS-II', 'card_capacity': '20G', 'sys': 'windows', 'i_format': 'CR2', 'i_avg': 20.11,
          'v_format': 'MOV', 'v_speed': 5.65, 'v_max': 'xxx', 'v_cut': 'xxx', 'capacity': 'xxx',
          'speed': 'NA', 'max_reso': '1920*1080', 'camera_num': 2, 'temper': '20', 'vol_ele': 'NA',
          'card_vol': '220V', 'per_img': 'xxx', 'character': 'xxx', 'state': '可使用', 'p_id': 'xxx',
          'begin': '2013', 'p_belong': 'xxx', 'price': 6666.66}]
    device = Device()
    for i in range(10):
        for i in d:
            d_type = DeviceType.objects.get(device_type=i.get('d_type'))
            d_state = State.objects.get(state=i.get('state'))
            self = device.add_device(
                d_type, i.get('d_id'), i.get('brand'),
                i.get('spec'), i.get('year'), i.get('support'),
                i.get('fw'), i.get('CPU'), i.get('card'),
                i.get('slog'), i.get('card_capacity'), i.get('sys'),
                i.get('i_format'), i.get('i_avg'), i.get('v_format'),
                i.get('v_speed'), i.get('v_max'), i.get('v_cut'),
                i.get('speed'), i.get('max_reso'),i.get('camera_num'),
                i.get('temper'), i.get('vol_ele'),i.get('card_vol'),
                i.get('per_img'), i.get('character'), d_state,
                i.get('p_id'), i.get('begin'), i.get('p_belong'),
                i.get('price'), ''
            )
            self.save()
    # return HttpResponseRedirect('/')


def new_test_record(request):
    d = [{'device_id': 1, 'user_id': 1}]
    record = TestRecord()
    for i in d:
        self = record.add_record(i.get('device_id'), i.get('user_id'), 1)
        self.save()
    # return HttpResponseRedirect('/')


def new_history(request):
    for i in range(30):
        new = TestRecord()
        new.device_id = 1
        new.user_id = 1
        new.version = '待填写'
        new.match = '待填写'
        new.card_num = 2
        new.card_id = '待填写'
        new.cycle = '待填写'
        new.compatibl = '待填写'
        new.number = 5
        new.fail_numb = 2
        new.SN = '待填写'
        new.result = '待填写'
        new.remark = '待填写'
        new.fail_pro = '待填写'
        new.compete = '待填写'
        new.record1 = '待填写'
        new.record2 = '待填写'
        new.JIRA = '待填写'
        new.save()
    # return redirect('/')


def new_task(request):
    name = '测试员1'
    task = AllotTasks.objects.filter(username=name)
    user = User.objects.filter(name=name)[0]
    for td in task:
        task_id = td.task_id
        device_list = td.test_device.split('/')
        for dev in device_list:
            d = Device.objects.filter(device_id=dev)[0]
            p = PersonalTask()
            p.task_id = task_id
            p.test_user = user
            p.test_device = d
            p.test_result = ''
            p.save()


# def new_parts(request):
    # ls = [{'type': }]


def all_do(request):
    new_tpye(request)
    new_group(request)
    new_job(request)
    new_state(request)

    return redirect('/')


def new_parts():
    path = str(os.path.abspath('.'))
    file_name = path + '\static\device_manage\配件信息表.xlsx'
    start_row = 2  # 起始行
    # 获取数据
    data = xlrd.open_workbook(file_name)
    camera = []
    sport_camera = []
    UAV = []
    switch = []
    # sheet-1
    table1 = data.sheet_by_name('相机配件信息表')
    nrows = table1.nrows
    for i in range(start_row, nrows):
        camera.append(table1.row_values(i))
    # sheet-2
    table2 = data.sheet_by_name('运动相机配件信息表')
    nrows = table2.nrows
    for i in range(start_row, nrows):
        sport_camera.append(table2.row_values(i))
    # sheet-3
    table3 = data.sheet_by_name('无人机配件信息表')
    nrows = table3.nrows
    for i in range(start_row, nrows):
        UAV.append(table3.row_values(i))
    # sheet-4
    table4 = data.sheet_by_name('Switch配件信息表')
    nrows = table4.nrows
    for i in range(start_row, nrows):
        switch.append(table4.row_values(i))
    print(camera)
    print(sport_camera)
    print(UAV)
    print(switch)
    for i in camera:
        new_parts = Parts()
        new_parts.type = DeviceType.objects.get(device_type='相机')
        new_parts.parts_type = i[1]
        new_parts.brand = i[2]
        new_parts.code = i[3]
        new_parts.num = int(i[4])
        new_parts.save()
    for i in sport_camera:
        new_parts = Parts()
        new_parts.type = DeviceType.objects.get(device_type='运动相机')
        new_parts.parts_type = i[1]
        new_parts.brand = i[2]
        new_parts.code = i[3]
        new_parts.num = int(i[4])
        new_parts.save()
    for i in UAV:
        new_parts = Parts()
        new_parts.type = DeviceType.objects.get(device_type='无人机')
        new_parts.parts_type = i[1]
        new_parts.brand = i[2]
        new_parts.code = i[3]
        new_parts.num = int(i[4])
        new_parts.save()
    for i in switch:
        new_parts = Parts()
        new_parts.type = DeviceType.objects.get(device_type='游戏机')
        new_parts.parts_type = i[1]
        new_parts.brand = i[2]
        new_parts.code = i[3]
        new_parts.num = int(i[4])
        new_parts.save()
    return redirect('/')


def many_device(path, types):
    file_path = path.replace('\\', '/')
    if types == '相机':
        this_type = DeviceType.objects.get(device_type=types)
        start_row = 4  # 起始行
        # 获取数据
        data = xlrd.open_workbook(file_path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            device = Device()
            device.device_state = State.objects.get(state='可使用')
            device.device_type = this_type
            device.device_id = data_ls[0]
            device.device_brand = data_ls[1]
            device.device_spec = data_ls[2]
            device.device_year = data_ls[3] if data_ls[3] else 0000
            device.device_property_id = data_ls[4]
            device.device_begin = data_ls[5]
            device.device_property_belong = data_ls[6]
            device.device_support = 0 if data_ls[7] == '✖' else 1
            device.device_fw_ver = data_ls[8]
            device.device_card = data_ls[9]
            device.device_card_capacity = data_ls[10]
            device.device_card_slog = data_ls[11]
            device.device_character = data_ls[12]
            device.remark = data_ls[13]
            device.device_price = data_ls[16]
            device.device_speed = data_ls[19]
            device.device_img_format = data_ls[20]
            device.device_img_avg = data_ls[23] if data_ls[23] else 0
            device.device_video_format = data_ls[24]
            device.device_video_speed = data_ls[25] if data_ls[25] else 0
            device.save()
            print('相机保存完成')
    elif types == '摄像机' or types == '运动相机':
        this_type = DeviceType.objects.get(device_type=types)
        start_row = 4  # 起始行
        # 获取数据
        data = xlrd.open_workbook(file_path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            device = Device()
            device.device_state = State.objects.get(state='可使用')
            device.device_type = this_type
            device.device_id = data_ls[0]
            device.device_brand = data_ls[1]
            device.device_spec = data_ls[2]
            device.device_year = data_ls[3] if data_ls[3] else 0000
            device.device_property_id = data_ls[4]
            device.device_begin = data_ls[5]
            device.device_property_belong = data_ls[6]
            device.device_support = 0 if data_ls[7] == '✖' else 1
            device.device_fw_ver = data_ls[8]
            device.device_card_capacity = data_ls[9]
            device.device_card_slog = data_ls[10]
            device.remark = data_ls[11]
            device.device_price = data_ls[15]
            device.device_speed = data_ls[17]
            device.device_img_format = data_ls[18]
            device.device_img_avg = data_ls[21] if data_ls[21] else 0
            device.device_video_format = data_ls[22]
            device.device_video_speed = data_ls[23] if data_ls[23] else 0
            device.save()
    elif types == '行车记录仪':
        this_type = DeviceType.objects.get(device_type=types)
        start_row = 3  # 起始行
        # 获取数据
        data = xlrd.open_workbook(file_path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            device = Device()
            device.device_type = this_type
            device.device_id = data_ls[0]
            device.device_brand = data_ls[1]
            device.device_spec = data_ls[2]
            device.CPU = data_ls[3]
            device.extra_capacity = data_ls[4]
            device.device_card_capacity = data_ls[5]
            device.device_speed = data_ls[6]
            device.device_camera_num = int(data_ls[7]) if data_ls[7] else 0
            device.device_max_reso = data_ls[8]
            device.voltage_electric = data_ls[9]
            device.card_voltage = data_ls[10]
            device.device_year = 0000
            device.device_price = data_ls[13]
            device.device_state = State.objects.get(state='可使用') \
                if data_ls[14] == '正常' or len(data_ls[14]) == 0 else State.objects.get(state='维护中')
            device.remark = data_ls[16]
            device.save()
    elif types == '监控':
        this_type = DeviceType.objects.get(device_type=types)
        start_row = 2  # 起始行
        # 获取数据
        data = xlrd.open_workbook(file_path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            device = Device()
            device.device_type = this_type
            device.device_id = data_ls[0]
            device.device_brand = data_ls[1]
            device.device_spec = data_ls[2]
            device.device_card_capacity = data_ls[3]
            device.extra_capacity = data_ls[4]
            device.device_speed = data_ls[5]
            device.device_temper = data_ls[6]
            device.device_price = data_ls[10]
            device.device_state = State.objects.get(state='可使用') \
                if data_ls[11] == '正常' or len(data_ls[11]) == 0 else State.objects.get(state='维护中')
            device.remark = data_ls[12] + '/' + data_ls[13]
            device.save()
    elif types == '无人机':
        this_type = DeviceType.objects.get(device_type=types)
        start_row = 4  # 起始行
        # 获取数据
        data = xlrd.open_workbook(file_path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            device = Device()
            device.device_state = State.objects.get(state='可使用')
            device.device_type = this_type
            device.device_brand = data_ls[0]
            device.device_id = '暂无'
            device.device_spec = data_ls[1]
            device.device_year = data_ls[2] if data_ls[2] else 0000
            device.device_support = 0 if data_ls[3] == '✖' else 1
            device.device_fw_ver = data_ls[4]
            device.device_card = data_ls[5]
            device.device_card_slog = data_ls[6]
            device.remark = data_ls[7]
            device.device_card_capacity = data_ls[12]
            device.device_speed = data_ls[13]
            device.device_sys = data_ls[14]
            device.device_video_format = data_ls[15]
            device.device_video_speed = data_ls[16] if data_ls[16] else 0
            device.save()
    elif types == '嵌入式设备':
        start_row = 2
        data = xlrd.open_workbook(file_path)
        os.remove(path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        for i in range(start_row, nrows):
            data_ls = sheet1.row_values(i)
            print(data_ls)
            for j in range(1, int(data_ls[8]) + 1):
                device = FlushDevice()
                device.platform = data_ls[0].replace('(', '（').replace(')', '）')
                device.num = j
                device.speed = data_ls[1]
                device.OEM = data_ls[2]
                device.ROM = data_ls[3]
                device.SOC = data_ls[4]
                device.SOC_spec = data_ls[5]
                device.sample_type = data_ls[6]
                device.system = data_ls[7]
                device.state = State.objects.get(state='可使用')
                device.save()
    elif types == '测试记录':
        start_table = 6
        data = xlrd.open_workbook(file_path)
        os.remove(path)
        sheet1 = data.sheets()[0]
        nrows = sheet1.nrows
        new_require = TestRequirements()
        new_require.init_time = datetime.datetime.now()
        new_require.end_time = datetime.datetime.now()
        new_require.start_time = datetime.datetime.now()
        new_require.finish_time = datetime.datetime.now()
        new_require.is_finished = 1
        new_require.save()
        device_ls = []
        for i in range(start_table, nrows):
            data_ls = sheet1.row_values(i)
            device = Device.objects.get(device_id=data_ls[0])
            device_ls.append(str(device.id))
            history_tester = User.objects.get(name='历史测试')
            result = data_ls[8]
            if result == 'PASS':
                result = True
                isNA = False
            elif result == 'FAIL':
                result = False
                isNA = False
            else:
                result = False
                isNA = True
            fail = data_ls[9]
            # 存入个人记录表
            person = PersonalTask()
            person.task = new_require
            person.test_device = device
            person.test_user = history_tester
            person.test_result = result
            person.fail_project = fail
            person.is_NA = isNA
            person.save()
            # 存入测试记录表
            record = TestRecord()
            record.task = new_require
            record.device = device
            record.user = history_tester
            record.result = result
            record.is_NA = isNA
            record.save()
        test_devices = '/'.join(device_ls)
        new_require.device = test_devices
        new_require.save()


def add_SN(request):
    file_path = os.path.abspath('.') + '/static/media/excel_data/SN编码规则_1231.xlsx'
    sheet = xlrd.open_workbook(file_path)
    start_row = 1
    # 主控表
    sheet1 = sheet.sheets()[1]
    end_row1 = sheet1.nrows
    for i in range(start_row, end_row1):
        data = sheet1.row_values(i)
        collocate = Collocation()
        collocate.collocation = data[0]
        collocate.num = data[1]
        collocate.category = 0
        collocate.save()

    # flash表
    sheet2 = sheet.sheets()[2]
    end_row2 = sheet2.nrows
    for i in range(start_row, end_row2):
        data = sheet2.row_values(i)
        collocate = Collocation()
        collocate.collocation = data[1]
        collocate.abbreviation = data[2]
        collocate.num = data[3]
        collocate.category = 1
        collocate.save()

    # 容量表
    sheet3 = sheet.sheets()[3]
    end_row3 = sheet3.nrows
    for i in range(start_row, end_row3):
        data = sheet3.row_values(i)
        if len(data[0]) != 0:
            die = Collocation()
            die.collocation = data[0]
            die.num = data[1]
            die.category = 2
            die.save()
            cap = Collocation()
            cap.abbreviation = data[2]
            cap.num = data[3]
            cap.category = 4
            cap.save()
        else:
            cap = Collocation()
            cap.abbreviation = data[2]
            cap.num = data[3]
            cap.category = 4
            cap.save()
    return redirect('/')
