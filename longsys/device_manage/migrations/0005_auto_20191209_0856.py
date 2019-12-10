# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0004_auto_20191208_2154'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrequirements',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, to='device_manage.User'),
        ),
        migrations.AlterField(
            model_name='testrequirements',
            name='finish_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
