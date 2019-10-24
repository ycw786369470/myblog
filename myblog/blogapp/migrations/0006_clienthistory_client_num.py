# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_remove_clienthistory_consume_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienthistory',
            name='client_num',
            field=models.IntegerField(default=1),
        ),
    ]
