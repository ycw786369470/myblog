from django.db import models
from utils import constants


# Create your models here.
class DeviceType(models.Model):
    device_type = models.CharField(max_length=20)           # 设备种类
    device_intro = models.CharField(max_length=20)          # 设备简介
    device_icon = models.CharField(max_length=50, null=True, blank=True)           # 图标路径

    def __str__(self):
        return self.device_type

    @classmethod
    def add_type(cls, type, intro):
        self = cls(device_type=type, device_intro=intro)
        return self


class State(models.Model):
    state = models.CharField(max_length=15)                             # 设备状态
    remark = models.CharField(max_length=50, blank=True)                # 备注

    def __str__(self):
        return self.state

    class Meta:
        verbose_name_plural = '设备状态'


class Device(models.Model):
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    device_type = models.ForeignKey(DeviceType)                         # 设备种类外键
    device_state = models.ForeignKey(State)                             # 设备状态
    device_id = models.CharField(max_length=20)                         # 设备编号
    device_brand = models.CharField(max_length=30)                      # 设备品牌
    device_spec = models.CharField(max_length=30)                       # 设备型号
    device_year = models.IntegerField(default=0)                        # 上市年份
    device_support = models.IntegerField(default=0)                     # 设备支持(0为不支持，1表示支持4k，2表示支持6k)
    device_fw_ver = models.CharField(max_length=20, null=True, blank=True)                     # 固件版本
    CPU = models.CharField(max_length=30, null=True, blank=True)                               # 处理器型号
    device_card = models.CharField(max_length=100, null=True, blank=True)                      # 支持卡型
    device_card_slog = models.CharField(max_length=20, null=True, blank=True)                  # 卡槽
    device_card_capacity = models.CharField(max_length=50, null=True, blank=True)              # 支持卡片容量
    device_sys = models.CharField(max_length=20, null=True, blank=True)                        # 支持文件系统
    device_img_format = models.CharField(max_length=10, null=True, blank=True)     # 图片格式
    device_img_avg = models.FloatField(default=0, null=True, blank=True)           # 图片平均速率
    device_video_format = models.CharField(max_length=10, null=True, blank=True)   # 视频格式
    device_video_speed = models.FloatField(default=0, null=True, blank=True)       # 视频速度
    device_video_max = models.CharField(max_length=50, null=True, blank=True)      # 最高录制设置
    device_video_cut = models.CharField(max_length=20, null=True, blank=True)      # 视屏文件分割
    device_speed = models.CharField(max_length=50, null=True, blank=True)                      # 速度要求
    device_max_reso = models.CharField(max_length=20, null=True, blank=True)                   # 最大分辨率
    device_camera_num = models.IntegerField(default=1, null=True, blank=True)                  # 镜头数量-
    device_temper = models.CharField(max_length=30, null=True, blank=True)         # 工作温度-
    voltage_electric = models.CharField(max_length=40, null=True, blank=True)      # 电源电压/电流-
    card_voltage = models.CharField(max_length=20, null=True, blank=True)          # 卡片电压-
    device_character = models.CharField(max_length=50, null=True, blank=True)      # 设备特性
    device_property_id = models.CharField(max_length=30, null=True, blank=True)    # 资产编号-
    device_begin = models.CharField(max_length=30, null=True, blank=True)          # 启用日期-
    device_property_belong = models.CharField(max_length=30, blank=True)           # 资产所属-
    device_price = models.CharField(max_length=50, default=0)                      # 购买价格-
    extra_capacity = models.CharField(blank=True, null=True, max_length=20)        # 扩展容量
    remark = models.CharField(blank=True, null=True, max_length=50)                # 备注
    is_problem = models.BooleanField(default=False)                                # 问题设备
    is_delete = models.BooleanField(default=False)                                 # 逻辑删除
    device_per_img = models.ImageField(upload_to='img', null=True, blank=True)     # 性能曲线图

    def __str__(self):
        return self.device_type.device_type + '  编号:' + self.device_id

    @classmethod
    def add_device(cls, d_type, d_id, brand, spec, year, support,
                   fw, CPU, card, slog, card_capacity, sys, i_format,
                   i_avg, v_format, v_speed, v_max, v_cut,
                   speed, max_reso, camera_num, temper, vol_ele, card_vol,
                   per_img, character, state, p_id, begin, p_belong, price,
                   extra):
        self = cls(
            device_type=d_type, device_id=d_id, device_brand=brand,
            device_spec=spec, device_year=year, device_support=support,
            device_fw_ver=fw, CPU=CPU,  device_card=card,
            device_card_slog=slog, device_card_capacity=card_capacity, device_sys=sys,
            device_img_format=i_format, device_img_avg=i_avg, device_video_format=v_format,
            device_video_speed=v_speed, device_video_max=v_max, device_video_cut=v_cut,
            device_speed=speed, device_max_reso=max_reso, device_camera_num=camera_num,
            device_temper=temper, voltage_electric=vol_ele, card_voltage=card_vol,
            device_per_img=per_img, device_character=character, device_state=state,
            device_property_id=p_id, device_begin=begin, device_property_belong=p_belong,
            device_price=price, extra_capacity=extra,
        )
        return self

    class Meta:
        verbose_name_plural = '设备信息'


# 岗位
class Job(models.Model):
    job_name = models.CharField(max_length=20)

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name_plural = "岗位"


# 小组
class Group(models.Model):
    group_name = models.CharField(max_length=30)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = '组别'


# 用户模型
class User(models.Model):
    password = models.CharField(max_length=100)                     # 密码
    group = models.ForeignKey(Group, blank=True)                    # 组名
    name = models.CharField(max_length=15)                          # 姓名
    job = models.ForeignKey(Job, blank=True)                        # 岗位
    is_admin = models.BooleanField(default=False)                   # 管理员身份
    is_init = models.BooleanField(default=False)                    # 需求发起身份
    last_login = models.DateTimeField(auto_now=True)                # 最晚登录时间
    regist_time = models.DateTimeField(auto_created=True)           # 注册时间
    staff_number = models.CharField(max_length=50, blank=False)     # 工号
    email = models.CharField(max_length=50, default='暂无')          # 邮箱

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '用户信息'


# 用户操作记录
class UserActionRecord(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(max_length=100)
    time = models.DateTimeField(auto_created=True)


class TestRequirements(models.Model):
    """ SD测试需求 """
    SN = models.CharField('SN编号', max_length=200, null=True)
    ver = models.CharField(max_length=30, default='暂未填写')                               # 版本
    match = models.CharField(max_length=50, default='暂未填写')                             # 搭配
    P_N = models.CharField(max_length=30, default='暂未填写')                               # 料号
    initiator = models.ForeignKey(User, default=1)                                        # 发起人
    device = models.CharField('测试设备', max_length=500, blank=True, null=True)
    sample_quantity = models.IntegerField('样品数量', default=0)
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    compatible_ver = models.CharField(max_length=20, default='暂未填写')                    # 兼容性测试版本
    remark = models.CharField(max_length=200, default='暂无', null=True, blank=True)          # 备注
    is_finished = models.NullBooleanField()
    file_path = models.CharField('上传fw包的路径', max_length=100, null=True, blank=True)
    is_rejected = models.BooleanField(default=False)                                        # 需求是否驳回
    reject_reason = models.CharField(max_length=100, blank=True, null=True)                 # 驳回原因
    rejecter = models.CharField(max_length=50, blank=True, null=True)                       # 驳回人姓名
    init_time = models.DateTimeField(auto_created=True)                                     # 发起时间
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'test_requirements'
        ordering = ['-reorder']


# SD测试记录表
class TestRecord(models.Model):
    device = models.ForeignKey(Device)                                         # 设备
    user = models.ForeignKey(User)                                             # 测试人
    task = models.ForeignKey(TestRequirements)
    version = models.CharField(max_length=30, default='暂未填写')                # 测试版本
    card_num = models.IntegerField(default=0)                                  # 卡数量
    card_id = models.CharField(max_length=30, default='')                      # 卡片编号
    number = models.IntegerField(default=0)                                    # 平台总数
    fail_number = models.IntegerField(default=0)                               # 失败平台数
    result = models.NullBooleanField()                                         # 测试结果
    remark = models.CharField(max_length=100, default='暂未填写')               # 备注
    fail_pro = models.CharField(max_length=200, default='暂未填写')             # 失败项目
    compete = models.CharField(max_length=100, default='暂未填写')              # 竞品对比
    record = models.CharField(max_length=200, default='暂未填写')               # 记录
    JIRA = models.CharField(max_length=100, default='暂未填写')                 # JIRA链接
    finish = models.DateTimeField(blank=True, null=True, auto_now=True)        # 完成时间
    is_NA = models.BooleanField(default=False)

    def __str__(self):
        return self.device.device_id + '的测试记录'

    @classmethod
    def add_record(cls, device, user, task):
        self = cls(device_id=device, user_id=user, task_id=task)
        return self


class RequirementsRecord(models.Model):
    task = models.ForeignKey(TestRequirements)              # 任务号
    device = models.ForeignKey(Device)                      # 设备号
    allot = models.ForeignKey(User, null=True, blank=True)  # 分配情况，空则为没分配，否则为被分配的user

    @classmethod
    def add_record(cls, task, device, allot):
        self = cls(task=task, device=device, allot=allot)
        return self


class AllotTasks(models.Model):
    """ SD任务分配 """
    # 复合关联
    task = models.ForeignKey(TestRequirements)
    user = models.ForeignKey(User)                  # 分配人
    username = models.CharField('操作人姓名', max_length=60, null=True, blank=True)
    test_device = models.CharField('测试的设备', max_length=300)
    is_finish = models.BooleanField(default=False)  # 任务是否完成
    finish_time = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        db_table = 'allot_tasks'


class PersonalTask(models.Model):
    """ SD个人任务表 """
    task = models.ForeignKey(TestRequirements)
    test_user = models.ForeignKey(User)
    test_device = models.ForeignKey(Device)
    test_result = models.NullBooleanField()
    record = models.CharField(max_length=200, blank=True, null=True, default='')    # 记录
    record_time = models.DateTimeField(null=True, blank=True, auto_now=True)        # 记录时间
    finish_time = models.DateTimeField(null=True, blank=True, auto_now=True)
    fail_project = models.CharField(blank=True, max_length=100, default='')         # 失败项
    fail_step = models.CharField(blank=True, max_length=100, default='')            # 失败步骤
    is_NA = models.BooleanField(default=False)                                      # 是否是无结果

    @classmethod
    def add_task(cls, task, user, device):
        self = cls(
            task=task, test_user=user, test_device=device,
        )
        return self

    class Meta:
        db_table = 'personal_task'


class Parts(models.Model):
    """配件表"""
    type = models.ForeignKey(DeviceType)            # 配件类型
    parts_type = models.CharField(max_length=20, default='')    # 类型
    brand = models.CharField(max_length=20, default='')         # 品牌
    code = models.CharField(max_length=20, default='')          # 代码
    num = models.IntegerField(default=0)            # 配件数量


class Collocation(models.Model):
    """ SD搭配表 """
    collocation = models.CharField('主控/flash/die', max_length=50)
    num = models.CharField('编号', max_length=20)
    abbreviation = models.CharField('简称', max_length=50, null=True, blank=True)
    category = models.IntegerField(
        '类别',
        choices=constants.COLLO_TYPES_CHOICES,
        default=constants.MASTER_CONTROL
    )

    @classmethod
    def add(cls, args):
        self = cls(args)
        self.save()

    class Meta:
        db_table = 'task_collocation'


# 兼容性测试版本
class CompatibleVer(models.Model):
    ver = models.CharField(max_length=30)
    step = models.CharField(max_length=300)

    def __str__(self):
        return self.ver

    class Meta:
        verbose_name_plural = '兼容性测试版本'


class UserIpRecord(models.Model):
    user = models.ForeignKey(User)
    ip = models.CharField(max_length=20)
    login_times = models.IntegerField(default=0)    # 用户该ip登陆次数


# excel上传记录
class ExcelRecord(models.Model):
    user = models.ForeignKey(User)
    filename = models.CharField(max_length=50)
    time = models.DateTimeField(auto_created=True)


# ============================================================
# 嵌入式组设备表
class FlushDevice(models.Model):
    platform = models.CharField('平台编号', max_length=30)
    num = models.IntegerField('序号', default=0)      # 用于在类型内部的排序，加在型号之后作区分
    speed = models.CharField('速度模式', max_length=20)
    OEM = models.CharField('OEM品牌', max_length=20)
    ROM = models.CharField('ROM类型', max_length=20)
    SOC = models.CharField('SOC方案商', max_length=20)
    SOC_spec = models.CharField('SOC型号', max_length=20)
    sample_type = models.CharField('样机类型', max_length=20)
    system = models.CharField('操作系统', max_length=30)
    state = models.ForeignKey(State)

    def __str__(self):
        return self.platform


# 外借清单
class Borrow(models.Model):
    device = models.ForeignKey(FlushDevice)
    user = models.ForeignKey(User)
    out_date = models.DateTimeField()
    back_date = models.DateTimeField()
    reason = models.CharField(max_length=50)


# 报废清单
class ScrapDevices(models.Model):
    device = models.ForeignKey(FlushDevice)
    scrap_date = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100)


# 送测平台清单
class Send2Test(models.Model):
    device = models.ForeignKey(FlushDevice)
    remark = models.CharField('备注', max_length=50)


# 嵌入式主控表
class Control(models.Model):
    control = models.CharField('主控', max_length=20)


# Flash表
class Flash(models.Model):
    flash = models.CharField('flash', max_length=20)


# FW表
class FW(models.Model):
    fw = models.CharField('fw版本', max_length=20)


# 测试类别
class TestType(models.Model):
    test_type = models.CharField(max_length=10)


# 测试项目
class TestProject(models.Model):
    test_item_id = models.CharField(max_length=30)
    test_item = models.CharField(max_length=30)


# 嵌入式需求表
class FlushDemand(models.Model):
    device = models.ForeignKey(FlushDevice)
    initiator = models.ForeignKey(User)
    recipient = models.CharField('需求接收人', max_length=20)
    control = models.ForeignKey(Control)
    flash = models.ForeignKey(Flash)
    fw = models.ForeignKey(FW)
    capacity = models.CharField('容量', max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    test_type = models.ForeignKey(TestType)         # 测试类别
    remark = models.CharField(max_length=50, blank=True, null=True)
    test_project = models.CharField(max_length=50)


# 嵌入式测试记录表
class FlushTestRecord(models.Model):
    task = models.ForeignKey(FlushDevice)                                           # 需求ID
    device = models.ForeignKey(Device)                                              # 设备
    system_burning = models.CharField(max_length=20,blank=True,default='')          # 系统烧录
    reset = models.CharField(max_length=20,blank=True,default='')                   # 恢复出厂设置
    cold_boot = models.CharField(max_length=20,blank=True,default='')               # 冷启动
    hot_boot = models.CharField(max_length=20,blank=True,default='')                # 热启动
    dormancy = models.CharField(max_length=20,blank=True,default='')                # 休眠唤醒
    start_cw = models.CharField(max_length=20,blank=True,default='')                # 启动超稳
    rw_cw = models.CharField(max_length=20,blank=True,default='')                   # 读写超稳
    rw_ageing = models.CharField(max_length=20,blank=True,default='')               # 读写老化
    video_ageing = models.CharField(max_length=20,blank=True,default='')            # 视频老化
    filetest = models.CharField(max_length=20,blank=True,default='')                # FileTest
    monkeyTest = models.CharField(max_length=20,blank=True,default='')              # MonkeyTest
    apk_upgrade = models.CharField(max_length=20,blank=True,default='')             # apk升级
    exe_upgrade = models.CharField(max_length=20,blank=True,default='')             # exe升级