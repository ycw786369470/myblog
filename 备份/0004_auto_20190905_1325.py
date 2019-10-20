# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_bloguser_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=100),
        ),
    ]
