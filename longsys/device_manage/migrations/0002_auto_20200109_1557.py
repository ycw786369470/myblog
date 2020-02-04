# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本CV1.0.0',
            },
        ),
        migrations.CreateModel(
            name='CV110',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本CV1.1.0',
            },
        ),
        migrations.CreateModel(
            name='DrV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本DrV1.0.0',
            },
        ),
        migrations.CreateModel(
            name='DV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本DV1.0.0',
            },
        ),
        migrations.CreateModel(
            name='IV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本IV1.0.0',
            },
        ),
        migrations.CreateModel(
            name='MV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本MV1.0.0',
            },
        ),
        migrations.CreateModel(
            name='RV100',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('test_step', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': '测试版本RV1.0.0',
            },
        ),
        migrations.RenameModel(
            old_name='TestVer1',
            new_name='CompatibleVer',
        ),
        migrations.AlterModelOptions(
            name='compatiblever',
            options={'verbose_name_plural': '兼容性测试版本'},
        ),
        migrations.RenameField(
            model_name='compatiblever',
            old_name='test_step',
            new_name='ver',
        ),
        migrations.AlterField(
            model_name='collocation',
            name='category',
            field=models.IntegerField(verbose_name='类别', default=0, choices=[(0, '主控'), (1, 'flash'), (2, 'die')]),
        ),
    ]
