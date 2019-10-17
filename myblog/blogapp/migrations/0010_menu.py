# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0009_table_table_food'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('food_img', models.ImageField(blank=True, upload_to='canteen/')),
                ('food_price', models.FloatField(default=0)),
                ('food_intro', models.CharField(max_length=200)),
                ('food_num', models.IntegerField(default=0)),
                ('food_up', models.IntegerField(default=0)),
                ('food_sold', models.IntegerField(default=0)),
                ('canteen', models.ForeignKey(to='blogapp.Canteen')),
            ],
        ),
    ]
