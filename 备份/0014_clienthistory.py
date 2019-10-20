# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0013_auto_20191019_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('consume_time', models.DateTimeField(auto_now_add=True)),
                ('food', models.CharField(max_length=800)),
                ('price', models.FloatField()),
                ('paid', models.BooleanField(default=False)),
                ('canteen', models.ForeignKey(to='blogapp.Canteen')),
                ('client', models.ForeignKey(to='blogapp.Users')),
            ],
        ),
    ]
