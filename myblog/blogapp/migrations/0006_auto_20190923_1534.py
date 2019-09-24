# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0005_bloguser_visit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cantee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cantee_name', models.CharField(max_length=50)),
                ('cantee_boss', models.CharField(max_length=30)),
                ('cantee_num', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ClientHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('consume_time', models.DateTimeField(auto_now_add=True)),
                ('food', models.CharField(max_length=500)),
                ('price', models.FloatField()),
                ('is_over', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('table_num', models.IntegerField(default=8)),
                ('table_clients', models.IntegerField(default=0)),
                ('is_over', models.BooleanField(default=False)),
                ('canteen', models.ForeignKey(to='blogapp.Cantee')),
            ],
        ),
        migrations.AlterModelOptions(
            name='bloguser',
            options={'verbose_name_plural': '全部博客'},
        ),
    ]
