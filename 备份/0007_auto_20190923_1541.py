# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0006_auto_20190923_1534'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cantee',
            new_name='Canteen',
        ),
        migrations.RenameField(
            model_name='canteen',
            old_name='cantee_boss',
            new_name='canteen_boss',
        ),
        migrations.RenameField(
            model_name='canteen',
            old_name='cantee_name',
            new_name='canteen_name',
        ),
        migrations.RenameField(
            model_name='canteen',
            old_name='cantee_num',
            new_name='canteen_num',
        ),
        migrations.RenameField(
            model_name='table',
            old_name='canteen',
            new_name='canteen',
        ),
    ]
