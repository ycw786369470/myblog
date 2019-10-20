# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0010_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='food_name',
            field=models.CharField(max_length=30, default='暂无'),
        ),
    ]
