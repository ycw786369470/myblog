from django.db import models


# Create your models here.
class DeviceType(models.Model):
    device_type = models.CharField(max_length=20)           # 设备种类
    device_intro = models.CharField(max_length=20)          # 设备简介

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
    device_fw_ver = models.CharField(max_length=20)                     # 固件版本
    CPU = models.CharField(max_length=30)                               # 处理器型号
    device_card = models.CharField(max_length=100)                      # 支持卡型
    device_card_slog = models.CharField(max_length=20)                  # 卡槽
    device_card_capacity = models.CharField(max_length=10)              # 支持卡片容量
    device_sys = models.CharField(max_length=20)                        # 支持文件系统
    device_img_format = models.CharField(max_length=10, blank=True)     # 图片格式
    device_img_avg = models.FloatField(default=0, blank=True)           # 图片平均速率
    device_video_format = models.CharField(max_length=10, blank=True)   # 视频格式
    device_video_speed = models.FloatField(default=0, blank=True)       # 视频速度
    device_video_max = models.CharField(max_length=50, blank=True)      # 最高录制设置
    device_video_cut = models.CharField(max_length=20, blank=True)      # 视屏文件分割
    device_speed = models.CharField(max_length=50)                      # 速度要求
    device_max_reso = models.CharField(max_length=20, blank=True)       # 最大分辨率
    device_camera_num = models.IntegerField(default=1)                  # 镜头数量-
    device_temper = models.CharField(max_length=30, blank=True)         # 工作温度-
    voltage_electric = models.CharField(max_length=40, blank=True)      # 电源电压/电流-
    card_voltage = models.CharField(max_length=20)                      # 卡片电压-
    device_per_img = models.ImageField(upload_to='img', blank=True)     # 性能曲线图
    device_character = models.CharField(max_length=50, blank=True)      # 设备特性
    device_property_id = models.CharField(max_length=30, blank=True)    # 资产编号-
    device_begin = models.CharField(max_length=30, blank=True)          # 启用日期-
    device_property_belong = models.CharField(max_length=30, blank=True)           # 资产所属-
    device_price = models.FloatField(default=0)                         # 购买价格-

    def __str__(self):
        return self.device_type.device_type + '  编号:' + self.device_id

    @classmethod
    def add_device(cls, d_type, d_id, brand, spec, year, support,
                   fw, CPU, card, slog, card_capacity, sys, i_format,
                   i_avg, v_format, v_speed, v_max, v_cut,
                   speed, max_reso, camera_num, temper, vol_ele, card_vol,
                   per_img, character, state, p_id, begin, p_belong, price):
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
            device_price=price
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
    group_name = models.CharField(max_length=30)                 # 组名

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name_plural = '组别'


# 用户模型
class User(models.Model):
    # 员工表
    password = models.CharField(max_length=100)                     # 密码
    group = models.ForeignKey(Group, blank=True)                    # 组名
    name = models.CharField(max_length=15)                          # 姓名
    job = models.ForeignKey(Job, blank=True)                        # 岗位
    is_admin = models.BooleanField(default=False)                   # 管理员身份
    is_init = models.BooleanField(default=False)                    # 需求发起身份
    last_login = models.DateTimeField(auto_now=True)                # 最晚登录时间
    regist_time = models.DateTimeField(auto_created=True)           # 注册时间
    staff_number = models.CharField(max_length=50, blank=False)     # 工号

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = '用户信息'


# 用户操作记录
class UserActionRecord(models.Model):
    user = models.ForeignKey(User)
    action = models.CharField(max_length=100)
    time = models.DateTimeField(auto_created=True)


# 测试记录表
class TestRecord(models.Model):
    device = models.ForeignKey(Device)                                          # 链接设备
    user = models.ForeignKey(User)                                              # 链接用户
    version = models.CharField(max_length=30, default='暂未填写')               # 测试版本
    match = models.CharField(max_length=50, default='暂未填写')                 # 搭配
    card_num = models.IntegerField(default=0)                                   # 卡数量
    card_id = models.CharField(max_length=30, default='暂未填写')               # 卡片编号
    cycle = models.CharField(max_length=20, default='暂未填写')                 # 测试周期
    compatible_ver = models.CharField(max_length=20, default='暂未填写')        # 兼容性测试版本
    number = models.IntegerField(default=0)                                     # 平台总数
    fail_number = models.IntegerField(default=0)                                # 失败平台数
    SN = models.CharField(max_length=30, default='暂未填写')                    # SN
    result = models.BooleanField(blank=True, default='暂未填写')                                    # 测试结果
    remark = models.CharField(max_length=100, default='暂未填写')               # 备注
    fail_pro = models.CharField(max_length=200, default='暂未填写')             # 失败项目
    compete = models.CharField(max_length=100, default='暂未填写')              # 竞争对比
    record1 = models.CharField(max_length=200, default='暂未填写')              # 记录1
    record2 = models.CharField(max_length=200, blank=True)                      # 记录2
    JIRA = models.CharField(max_length=100, default='暂未填写')                 # JIRA链接
    finish = models.DateTimeField(blank=True, null=True)                        # 完成时间
    # 编号/品牌/型号/支持4k/卡槽在Device表中

    def __str__(self):
        return self.device.device_id + '的测试记录'

    @classmethod
    def add_record(cls, device, user):
        self = cls(device_id=device, user_id=user)
        return self


class TestReport(models.Model):
    device = models.ForeignKey(Device)                      # 链接设备
    user = models.ForeignKey(User)                          # 链接用户
    version = models.CharField(max_length=30)               # 测试版本
    match = models.CharField(max_length=50)                 # 搭配
    card_num = models.IntegerField(default=0)               # 卡数量
    card_id = models.CharField(max_length=30)               # 卡片编号
    cycle = models.CharField(max_length=20)                 # 测试周期
    compatible_ver = models.CharField(max_length=20)        # 兼容性测试版本
    number = models.IntegerField(default=0)                 # 平台总数
    fail_number = models.IntegerField(default=0)            # 失败平台数
    SN = models.CharField(max_length=30)                    # SN编号
    result = models.CharField(max_length=300)               # 结果
    remark = models.CharField(max_length=100)               # 备注
    fail_pro = models.CharField(max_length=200)             # 失败项目
    JIRA = models.CharField(max_length=100)                 # JIRA链接
    # 编号/品牌/型号/支持4k/卡槽在Device表中


class TestRequirements(models.Model):
    """ 测试需求 """
    # task_id = models.CharField(max_length=20,null=True,blank=True)
    SN = models.CharField('SN编号', max_length=200, null=True)
    device = models.CharField('测试设备', max_length=500, blank=True)
    start_time = models.DateTimeField('开始时间', null=True, blank=True)
    end_time = models.DateTimeField('结束时间', null=True, blank=True)
    sample_quantity = models.IntegerField('样品数量', default=0)
    reorder = models.SmallIntegerField('排序', default=0, help_text='数字越大，越靠前')
    manager = models.ForeignKey(User, null=True, blank=True)            # 经手人
    is_finished = models.NullBooleanField()
    finish_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'test_requirements'
        ordering = ['-reorder']


class RequirementsRecord(models.Model):
    """测试需求中间表，记录设备分配情况"""
    task = models.ForeignKey(TestRequirements)              # 任务号
    device = models.ForeignKey(Device)                      # 设备号
    allot = models.ForeignKey(User, null=True, blank=True)  # 分配情况，空则为没分配，否则为被分配的user


class AllotTasks(models.Model):
    """ 任务分配 """
    # 复合关联
    task_id = models.ForeignKey(TestRequirements)
    user = models.ForeignKey(User)                  # 发布者
    username = models.CharField('操作人姓名', max_length=60, null=True, blank=True)
    test_device = models.CharField('测试的设备', max_length=300)
    is_finished = models.NullBooleanField()
    finish_time = models.DateTimeField()

    class Meta:
        db_table = 'allot_tasks'


class PersonalTask(models.Model):
    """ 个人任务表 """
    # 复合关联
    task_id = models.ForeignKey(TestRequirements)
    test_user = models.ForeignKey(User)
    test_device = models.ForeignKey(Device)
    test_record = models.CharField(max_length=200)      # 记录
    finish_time = models.DateTimeField()
    is_finished = models.NullBooleanField()             # 测试是否完成-null:待测/False:失败/True:通过

    class Meta:
        db_table = 'personal_task'















