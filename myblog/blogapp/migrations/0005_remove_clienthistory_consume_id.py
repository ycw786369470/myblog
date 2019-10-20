# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_clienthistory_consume_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clienthistory',
            name='consume_id',
        ),
    ]
