# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=30)),
                ('content', DjangoUeditor.models.UEditorField()),
                ('time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '博客用户',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('category_name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField()),
                ('time', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': '评论',
            },
        ),
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('web_img', models.ImageField(upload_to='blog/')),
                ('web_name', models.CharField(max_length=100)),
                ('url', models.URLField()),
                ('introduce', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('up_num', models.IntegerField(default=0)),
                ('down_num', models.IntegerField(default=0)),
                ('star_num', models.IntegerField(default=0)),
            ],
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
                ('adv', models.BooleanField(verbose_name='是否为广告位推广', default=False)),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='标题', max_length=100)),
                ('content', models.CharField(verbose_name='内容', max_length=100)),
                ('delete', models.BooleanField(default=False)),
                ('cteated_time', models.DateTimeField(verbose_name='创建时间')),
                ('modified_time', models.DateTimeField(verbose_name='发布时间')),
                ('category', models.ForeignKey(to='blogapp.Category')),
            ],
            options={
                'verbose_name_plural': '博客',
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
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('tag_name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('picture', models.ImageField(upload_to='blog/')),
            ],
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
        migrations.CreateModel(
            name='UserDown',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_over', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('photo', models.ImageField(blank=True, upload_to='blog/')),
                ('thumb', models.ImageField(blank=True, upload_to='thumb/')),
                ('name', models.CharField(max_length=25)),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
                ('gender', models.BooleanField(default=True)),
                ('habits', models.ForeignKey(to='blogapp.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='UserStar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_over', models.BooleanField(default=False)),
                ('mark_name', models.ForeignKey(to='blogapp.Users')),
                ('name', models.ForeignKey(to='blogapp.BlogUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('is_over', models.BooleanField(default=False)),
                ('mark_name', models.ForeignKey(to='blogapp.Users')),
                ('name', models.ForeignKey(to='blogapp.BlogUser')),
            ],
        ),
        migrations.AddField(
            model_name='userdown',
            name='mark_name',
            field=models.ForeignKey(to='blogapp.Users'),
        ),
        migrations.AddField(
            model_name='userdown',
            name='name',
            field=models.ForeignKey(to='blogapp.BlogUser'),
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, to='blogapp.Tag'),
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
        migrations.AddField(
            model_name='mark',
            name='mark_name',
            field=models.ForeignKey(to='blogapp.Users'),
        ),
        migrations.AddField(
            model_name='mark',
            name='name',
            field=models.ForeignKey(to='blogapp.BlogUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='name',
            field=models.ForeignKey(to='blogapp.Users'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='blogapp.BlogUser'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='name',
            field=models.ForeignKey(to='blogapp.Users'),
        ),
        migrations.AddField(
            model_name='bloguser',
            name='tag',
            field=models.ForeignKey(to='blogapp.Tag'),
        ),
    ]
