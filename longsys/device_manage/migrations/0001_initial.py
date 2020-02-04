# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AllotTasks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(verbose_name='操作人姓名', max_length=60, blank=True, null=True)),
                ('test_device', models.CharField(verbose_name='测试的设备', max_length=300)),
                ('is_finish', models.BooleanField(default=False)),
                ('finish_time', models.DateTimeField(null=True, auto_now=True)),
            ],
            options={
                'db_table': 'allot_tasks',
            },
        ),
        migrations.CreateModel(
            name='Collocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('collocation', models.CharField(verbose_name='主控/flash/die', max_length=50)),
                ('num', models.CharField(verbose_name='编号', max_length=20)),
                ('abbreviation', models.CharField(verbose_name='简称', max_length=50, blank=True, null=True)),
                ('category', models.SmallIntegerField(verbose_name='类别', default=0, choices=[(0, '主控'), (1, 'flash'), (2, 'die')])),
            ],
            options={
                'db_table': 'task_collocation',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('reorder', models.SmallIntegerField(verbose_name='排序', default=0, help_text='数字越大，越靠前')),
                ('device_id', models.CharField(max_length=20)),
                ('device_brand', models.CharField(max_length=30)),
                ('device_spec', models.CharField(max_length=30)),
                ('device_year', models.IntegerField(default=0)),
                ('device_support', models.IntegerField(default=0)),
                ('device_fw_ver', models.CharField(max_length=20, blank=True, null=True)),
                ('CPU', models.CharField(max_length=30, blank=True, null=True)),
                ('device_card', models.CharField(max_length=100, blank=True, null=True)),
                ('device_card_slog', models.CharField(max_length=20, blank=True, null=True)),
                ('device_card_capacity', models.CharField(max_length=50, blank=True, null=True)),
                ('device_sys', models.CharField(max_length=20, blank=True, null=True)),
                ('device_img_format', models.CharField(max_length=10, blank=True, null=True)),
                ('device_img_avg', models.FloatField(blank=True, null=True, default=0)),
                ('device_video_format', models.CharField(max_length=10, blank=True, null=True)),
                ('device_video_speed', models.FloatField(blank=True, null=True, default=0)),
                ('device_video_max', models.CharField(max_length=50, blank=True, null=True)),
                ('device_video_cut', models.CharField(max_length=20, blank=True, null=True)),
                ('device_speed', models.CharField(max_length=50, blank=True, null=True)),
                ('device_max_reso', models.CharField(max_length=20, blank=True, null=True)),
                ('device_camera_num', models.IntegerField(blank=True, null=True, default=1)),
                ('device_temper', models.CharField(max_length=30, blank=True, null=True)),
                ('voltage_electric', models.CharField(max_length=40, blank=True, null=True)),
                ('card_voltage', models.CharField(max_length=20, blank=True, null=True)),
                ('device_character', models.CharField(max_length=50, blank=True, null=True)),
                ('device_property_id', models.CharField(max_length=30, blank=True, null=True)),
                ('device_begin', models.CharField(max_length=30, blank=True, null=True)),
                ('device_property_belong', models.CharField(max_length=30, blank=True)),
                ('device_price', models.CharField(max_length=50, default=0)),
                ('extra_capacity', models.CharField(max_length=20, blank=True, null=True)),
                ('remark', models.CharField(max_length=50, blank=True, null=True)),
                ('is_problem', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('device_per_img', models.ImageField(blank=True, null=True, upload_to='img')),
            ],
            options={
                'verbose_name_plural': '设备信息',
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('device_type', models.CharField(max_length=20)),
                ('device_intro', models.CharField(max_length=20)),
                ('device_icon', models.CharField(max_length=50, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExcelRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_created=True)),
                ('filename', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('group_name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '组别',
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('job_name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': '岗位',
            },
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('parts_type', models.CharField(max_length=20, default='')),
                ('brand', models.CharField(max_length=20, default='')),
                ('code', models.CharField(max_length=20, default='')),
                ('num', models.IntegerField(default=0)),
                ('type', models.ForeignKey(to='device_manage.DeviceType')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_result', models.NullBooleanField()),
                ('record', models.CharField(max_length=200, blank=True, null=True, default='')),
                ('record_time', models.DateTimeField(null=True, auto_now=True)),
                ('finish_time', models.DateTimeField(null=True, auto_now=True)),
                ('fail_project', models.CharField(max_length=100, blank=True, default='')),
                ('fail_step', models.CharField(max_length=100, blank=True, default='')),
            ],
            options={
                'db_table': 'personal_task',
            },
        ),
        migrations.CreateModel(
            name='RequirementsRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('state', models.CharField(max_length=15)),
                ('remark', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'verbose_name_plural': '设备状态',
            },
        ),
        migrations.CreateModel(
            name='TestRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('version', models.CharField(max_length=30, default='暂未填写')),
                ('card_num', models.IntegerField(default=0)),
                ('card_id', models.CharField(max_length=30, default='')),
                ('number', models.IntegerField(default=0)),
                ('fail_number', models.IntegerField(default=0)),
                ('result', models.NullBooleanField()),
                ('remark', models.CharField(max_length=100, default='暂未填写')),
                ('fail_pro', models.CharField(max_length=200, default='暂未填写')),
                ('compete', models.CharField(max_length=100, default='暂未填写')),
                ('record', models.CharField(max_length=200, default='暂未填写')),
                ('JIRA', models.CharField(max_length=100, default='暂未填写')),
                ('finish', models.DateTimeField(null=True, auto_now=True)),
                ('device', models.ForeignKey(to='device_manage.Device')),
            ],
        ),
        migrations.CreateModel(
            name='TestRequirements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('init_time', models.DateTimeField(auto_created=True)),
                ('SN', models.CharField(verbose_name='SN编号', max_length=200, null=True)),
                ('ver', models.CharField(max_length=30, default='暂未填写')),
                ('match', models.CharField(max_length=50, default='暂未填写')),
                ('P_N', models.CharField(max_length=30, default='暂未填写')),
                ('device', models.CharField(verbose_name='测试设备', max_length=500, blank=True, null=True)),
                ('start_time', models.DateTimeField(verbose_name='开始时间', blank=True, null=True)),
                ('end_time', models.DateTimeField(verbose_name='结束时间', blank=True, null=True)),
                ('sample_quantity', models.IntegerField(verbose_name='样品数量', default=0)),
                ('reorder', models.SmallIntegerField(verbose_name='排序', default=0, help_text='数字越大，越靠前')),
                ('compatible_ver', models.CharField(max_length=20, default='暂未填写')),
                ('remark', models.CharField(max_length=200, blank=True, null=True, default='暂无')),
                ('is_finished', models.NullBooleanField()),
                ('finish_time', models.DateTimeField(null=True, auto_now=True)),
                ('file_path', models.CharField(verbose_name='上传fw包的路径', max_length=100, blank=True, null=True)),
                ('is_rejected', models.BooleanField(default=False)),
                ('reject_reason', models.CharField(max_length=100, blank=True, null=True)),
                ('rejecter', models.CharField(max_length=50, blank=True, null=True)),
            ],
            options={
                'db_table': 'test_requirements',
                'ordering': ['-reorder'],
            },
        ),
        migrations.CreateModel(
            name='TestVer1',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本1',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('regist_time', models.DateTimeField(auto_created=True)),
                ('password', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=15)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_init', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('staff_number', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, default='暂无')),
                ('group', models.ForeignKey(blank=True, to='device_manage.Group')),
                ('job', models.ForeignKey(blank=True, to='device_manage.Job')),
            ],
            options={
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.CreateModel(
            name='UserActionRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_created=True)),
                ('action', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to='device_manage.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserIpRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip', models.CharField(max_length=20)),
                ('login_times', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='device_manage.User')),
            ],
        ),
        migrations.AddField(
            model_name='testrequirements',
            name='initiator',
            field=models.ForeignKey(default=1, to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='task',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='requirementsrecord',
            name='allot',
            field=models.ForeignKey(blank=True, null=True, to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='requirementsrecord',
            name='device',
            field=models.ForeignKey(to='device_manage.Device'),
        ),
        migrations.AddField(
            model_name='requirementsrecord',
            name='task',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='task',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='test_device',
            field=models.ForeignKey(to='device_manage.Device'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='test_user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='excelrecord',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_state',
            field=models.ForeignKey(to='device_manage.State'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_type',
            field=models.ForeignKey(to='device_manage.DeviceType'),
        ),
        migrations.AddField(
            model_name='allottasks',
            name='task',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='allottasks',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
    ]
