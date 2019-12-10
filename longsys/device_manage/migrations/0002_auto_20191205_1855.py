# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='device_capacity',
        ),
        migrations.AlterField(
            model_name='personaltask',
            name='test_device',
            field=models.ForeignKey(to='device_manage.Device'),
        ),
    ]
