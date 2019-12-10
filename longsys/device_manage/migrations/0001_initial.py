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
                ('test_device', models.CharField(verbose_name='测试的设备', max_length=200)),
            ],
            options={
                'db_table': 'allot_tasks',
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
                ('device_fw_ver', models.CharField(max_length=20)),
                ('CPU', models.CharField(max_length=30)),
                ('device_card', models.CharField(max_length=100)),
                ('device_card_slog', models.CharField(max_length=20)),
                ('device_card_capacity', models.CharField(max_length=10)),
                ('device_sys', models.CharField(max_length=20)),
                ('device_img_format', models.CharField(max_length=10, blank=True)),
                ('device_img_avg', models.FloatField(blank=True, default=0)),
                ('device_video_format', models.CharField(max_length=10, blank=True)),
                ('device_video_speed', models.FloatField(blank=True, default=0)),
                ('device_video_max', models.CharField(max_length=50, blank=True)),
                ('device_video_cut', models.CharField(max_length=20, blank=True)),
                ('device_capacity', models.CharField(max_length=30, blank=True)),
                ('device_speed', models.CharField(max_length=50)),
                ('device_max_reso', models.CharField(max_length=20, blank=True)),
                ('device_camera_num', models.IntegerField(default=1)),
                ('device_temper', models.CharField(max_length=30, blank=True)),
                ('voltage_electric', models.CharField(max_length=40, blank=True)),
                ('card_voltage', models.CharField(max_length=20)),
                ('device_per_img', models.ImageField(blank=True, upload_to='img')),
                ('device_character', models.CharField(max_length=50, blank=True)),
                ('device_property_id', models.CharField(max_length=30, blank=True)),
                ('device_begin', models.CharField(max_length=30, blank=True)),
                ('device_property_belong', models.CharField(max_length=30, blank=True)),
                ('device_price', models.FloatField(default=0)),
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
            name='PersonalTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
            ],
            options={
                'db_table': 'personal_task',
            },
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
                ('match', models.CharField(max_length=50, default='暂未填写')),
                ('card_num', models.IntegerField(default=0)),
                ('card_id', models.CharField(max_length=30, default='暂未填写')),
                ('cycle', models.CharField(max_length=20, default='暂未填写')),
                ('compatible_ver', models.CharField(max_length=20, default='暂未填写')),
                ('number', models.IntegerField(default=0)),
                ('fail_number', models.IntegerField(default=0)),
                ('SN', models.CharField(max_length=30, default='暂未填写')),
                ('result', models.BooleanField(default='暂未填写')),
                ('remark', models.CharField(max_length=100, default='暂未填写')),
                ('fail_pro', models.CharField(max_length=200, default='暂未填写')),
                ('compete', models.CharField(max_length=100, default='暂未填写')),
                ('record1', models.CharField(max_length=200, default='暂未填写')),
                ('record2', models.CharField(max_length=200, blank=True)),
                ('JIRA', models.CharField(max_length=100, default='暂未填写')),
                ('finish', models.DateTimeField(blank=True, null=True)),
                ('device', models.ForeignKey(to='device_manage.Device')),
            ],
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('version', models.CharField(max_length=30)),
                ('match', models.CharField(max_length=50)),
                ('card_num', models.IntegerField(default=0)),
                ('card_id', models.CharField(max_length=30)),
                ('cycle', models.CharField(max_length=20)),
                ('compatible_ver', models.CharField(max_length=20)),
                ('number', models.IntegerField(default=0)),
                ('fail_number', models.IntegerField(default=0)),
                ('SN', models.CharField(max_length=30)),
                ('result', models.CharField(max_length=300)),
                ('remark', models.CharField(max_length=100)),
                ('fail_pro', models.CharField(max_length=200)),
                ('JIRA', models.CharField(max_length=100)),
                ('device', models.ForeignKey(to='device_manage.Device')),
            ],
        ),
        migrations.CreateModel(
            name='TestRequirements',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('SN', models.CharField(verbose_name='SN编号', max_length=200, null=True)),
                ('device', models.CharField(verbose_name='测试设备', max_length=500, blank=True)),
                ('start_time', models.DateTimeField(verbose_name='开始时间', blank=True, null=True)),
                ('end_time', models.DateTimeField(verbose_name='结束时间', blank=True, null=True)),
                ('sample_quantity', models.IntegerField(verbose_name='样品数量', default=0)),
                ('reorder', models.SmallIntegerField(verbose_name='排序', default=0, help_text='数字越大，越靠前')),
            ],
            options={
                'db_table': 'test_requirements',
                'ordering': ['-reorder'],
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
        migrations.AddField(
            model_name='testreport',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='task_id',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='test_device',
            field=models.ForeignKey(to='device_manage.TestRecord'),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='test_user',
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
            name='task_id',
            field=models.ForeignKey(to='device_manage.TestRequirements'),
        ),
        migrations.AddField(
            model_name='allottasks',
            name='user',
            field=models.ForeignKey(to='device_manage.User'),
        ),
    ]
