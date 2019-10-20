# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_remove_bloguser_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='content',
            field=DjangoUeditor.models.UEditorField(default=datetime.datetime(2019, 9, 5, 2, 40, 53, 475521, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
