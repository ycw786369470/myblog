# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_clienthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienthistory',
            name='table',
            field=models.IntegerField(default=0),
        ),
    ]
