# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_auto_20190822_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='thumb',
            field=models.ImageField(blank=True, upload_to='thumb/'),
        ),
    ]
