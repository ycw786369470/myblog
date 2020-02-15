# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0002_auto_20200214_1115'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CV100',
        ),
        migrations.DeleteModel(
            name='CV110',
        ),
        migrations.DeleteModel(
            name='DrV100',
        ),
        migrations.DeleteModel(
            name='DV100',
        ),
        migrations.DeleteModel(
            name='IV100',
        ),
        migrations.DeleteModel(
            name='MV100',
        ),
        migrations.DeleteModel(
            name='RV100',
        ),
        migrations.AddField(
            model_name='compatiblever',
            name='step',
            field=models.CharField(max_length=300, default=datetime.datetime(2020, 2, 15, 17, 30, 5, 89962)),
            preserve_default=False,
        ),
    ]
