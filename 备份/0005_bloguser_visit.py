# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_auto_20190905_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='visit',
            field=models.IntegerField(default=0),
        ),
    ]
