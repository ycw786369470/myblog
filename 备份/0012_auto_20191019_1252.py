# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0011_menu_food_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': '菜单'},
        ),
        migrations.RenameField(
            model_name='clienthistory',
            old_name='is_over',
            new_name='paid',
        ),
        migrations.AddField(
            model_name='clienthistory',
            name='canteen',
            field=models.ForeignKey(default=datetime.datetime(2019, 10, 19, 4, 52, 34, 757809, tzinfo=utc), to='blogapp.Canteen'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clienthistory',
            name='client',
            field=models.ForeignKey(default=datetime.datetime(2019, 10, 19, 4, 52, 44, 279672, tzinfo=utc), to='blogapp.Users'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clienthistory',
            name='food',
            field=models.CharField(max_length=800),
        ),
        migrations.AlterField(
            model_name='menu',
            name='food_img',
            field=models.ImageField(blank=True, upload_to='canteen/img/'),
        ),
    ]
