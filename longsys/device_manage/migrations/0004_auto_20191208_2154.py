# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0003_auto_20191208_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='testrequirements',
            name='finish_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 12, 8, 13, 54, 45, 347965, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testrequirements',
            name='is_finished',
            field=models.NullBooleanField(),
        ),
    ]
