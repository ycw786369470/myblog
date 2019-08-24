# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('web_name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('introduce', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=1000)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '留言',
            },
        ),
        migrations.CreateModel(
            name='NewBlog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=50)),
                ('classfy', models.CharField(verbose_name='分类', max_length=20, choices=[('网站前端', '网站前端'), ('后端技术', '后端技术')])),
                ('source', models.CharField(verbose_name='来源', max_length=50)),
                ('look', models.IntegerField(verbose_name='围观次数', default=0)),
                ('content', DjangoUeditor.models.UEditorField()),
                ('pub_time', models.DateTimeField(verbose_name='发布时间', auto_now_add=True)),
                ('mod_time', models.DateTimeField(verbose_name='修改时间', auto_now=True)),
                ('img', models.ImageField(upload_to='')),
                ('adv', models.BooleanField(verbose_name='广告位', default=False)),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name_plural': '每日一句',
            },
        ),
        migrations.CreateModel(
            name='Us',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('QQ', models.CharField(max_length=15)),
                ('QQgroup', models.CharField(max_length=15)),
                ('content', models.CharField(max_length=1000)),
                ('email', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': '关于我们',
            },
        ),
        migrations.AlterField(
            model_name='users',
            name='photo',
            field=models.ImageField(blank=True, upload_to='blog/'),
        ),
        migrations.AddField(
            model_name='newblog',
            name='author',
            field=models.ForeignKey(to='blogapp.Users'),
        ),
        migrations.AddField(
            model_name='newblog',
            name='tags',
            field=models.ManyToManyField(to='blogapp.Tag'),
        ),
    ]
