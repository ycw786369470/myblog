# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlushTestRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('system_burning', models.CharField(max_length=20, blank=True, default='')),
                ('reset', models.CharField(max_length=20, blank=True, default='')),
                ('cold_boot', models.CharField(max_length=20, blank=True, default='')),
                ('hot_boot', models.CharField(max_length=20, blank=True, default='')),
                ('dormancy', models.CharField(max_length=20, blank=True, default='')),
                ('start_cw', models.CharField(max_length=20, blank=True, default='')),
                ('rw_cw', models.CharField(max_length=20, blank=True, default='')),
                ('rw_ageing', models.CharField(max_length=20, blank=True, default='')),
                ('video_ageing', models.CharField(max_length=20, blank=True, default='')),
                ('filetest', models.CharField(max_length=20, blank=True, default='')),
                ('monkeyTest', models.CharField(max_length=20, blank=True, default='')),
                ('apk_upgrade', models.CharField(max_length=20, blank=True, default='')),
                ('exe_upgrade', models.CharField(max_length=20, blank=True, default='')),
                ('device', models.ForeignKey(to='device_manage.Device')),
            ],
        ),
        migrations.RemoveField(
            model_name='embedtestrecord',
            name='device',
        ),
        migrations.RemoveField(
            model_name='embedtestrecord',
            name='task',
        ),
        migrations.AddField(
            model_name='flushdevice',
            name='num',
            field=models.IntegerField(verbose_name='序号', default=0),
        ),
        migrations.DeleteModel(
            name='EmbedTestRecord',
        ),
        migrations.AddField(
            model_name='flushtestrecord',
            name='task',
            field=models.ForeignKey(to='device_manage.FlushDevice'),
        ),
    ]
