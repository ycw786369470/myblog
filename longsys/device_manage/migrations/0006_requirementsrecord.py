# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('device_manage', '0005_auto_20191209_0856'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequirementsRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('allot', models.ForeignKey(blank=True, null=True, to='device_manage.User')),
                ('device', models.ForeignKey(to='device_manage.Device')),
                ('task', models.ForeignKey(to='device_manage.TestRequirements')),
            ],
        ),
    ]
