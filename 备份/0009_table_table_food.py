# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0008_users_is_boss'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='table_food',
            field=models.CharField(max_length=300, default='none'),
        ),
    ]
