# 该文件用来新建数据信息，转移至新的计算机启动前调用添加基本信息
from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from device_manage.models import *


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
    return redirect('/')


def new_state(request):
    d = ['可使用', '维护中', '无电池', '卡槽损坏', '借出', '租赁', '其他', '无充电器', '测试中']
    for i in d:
        new = State()
        new.state = i
        new.save()
    return redirect('/')


def new_job(request):
    d = ['实习生', '测试员', '测试主管', '助理测试工程师', '测试技工', '测试工程师', '其他']
    for i in d:
        new = Job()
        new.job_name = i
        new.save()
    return redirect('/')


def new_group(request):
    d = ['嵌入式', 'SSD', '移动存储', '微存储', '其他']
    for i in d:
        new = Group()
        new.group_name = i
        new.save()
    return redirect('/')


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
                i.get('price')
            )
            self.save()
    return HttpResponseRedirect('/')


def new_test_record(request):
    d = [{'device_id': 1, 'user_id': 1}]
    record = TestRecord()
    for i in d:
        self = record.add_record(i.get('device_id'), i.get('user_id'))
        self.save()
    return HttpResponseRedirect('/')
