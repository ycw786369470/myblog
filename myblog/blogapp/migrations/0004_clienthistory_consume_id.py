# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0003_clienthistory_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienthistory',
            name='consume_id',
            field=models.IntegerField(default=1000, auto_created=True),
        ),
    ]
