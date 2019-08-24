# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0002_auto_20190821_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendlink',
            name='web_img',
            field=models.ImageField(default=datetime.datetime(2019, 8, 22, 6, 39, 1, 969214, tzinfo=utc), upload_to='blog/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='newblog',
            name='adv',
            field=models.BooleanField(verbose_name='是否为广告位推广', default=False),
        ),
    ]
