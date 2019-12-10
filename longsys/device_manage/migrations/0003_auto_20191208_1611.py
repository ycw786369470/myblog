# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0002_auto_20191205_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='allottasks',
            name='finish_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 8, 7, 53, 47, 897645, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='allottasks',
            name='is_finished',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='finish_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 8, 7, 53, 52, 291387, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personaltask',
            name='is_finished',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='personaltask',
            name='test_record',
            field=models.CharField(max_length=200, default=datetime.datetime(2019, 12, 8, 8, 11, 5, 177918, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='allottasks',
            name='test_device',
            field=models.CharField(verbose_name='测试的设备', max_length=300),
        ),
    ]
