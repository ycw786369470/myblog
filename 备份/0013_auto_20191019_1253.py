# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0012_auto_20191019_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clienthistory',
            name='canteen',
        ),
        migrations.RemoveField(
            model_name='clienthistory',
            name='client',
        ),
        migrations.DeleteModel(
            name='ClientHistory',
        ),
    ]
