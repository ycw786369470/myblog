# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0007_auto_20190923_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_boss',
            field=models.BooleanField(default=False),
        ),
    ]
