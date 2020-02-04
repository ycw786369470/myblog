# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0002_auto_20200109_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='personaltask',
            name='is_NA',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='testrecord',
            name='is_NA',
            field=models.BooleanField(default=False),
        ),
    ]
