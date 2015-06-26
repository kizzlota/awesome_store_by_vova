# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import django.utils.timezone
import catalog.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, numbers and @/./+/-/_ characters', unique=True, max_length=50)),
                ('email', models.EmailField(max_length=255, unique=True, null=True)),
                ('first_name', models.CharField(max_length=30, null=True, blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('social_img_url', models.CharField(max_length=120, null=True, blank=True)),
                ('profile_image', models.ImageField(default=b'/static/img/users/defaultuserimage.png', upload_to=b'uploads')),
                ('user_bio', models.TextField(max_length=1200, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='catalog.Category', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('main_image', models.ImageField(default=b'/static/img/shoesimage.jpg', null=True, upload_to=catalog.models.get_file_path, blank=True)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=150, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('quantity', models.IntegerField(default=0)),
                ('category_name', models.ManyToManyField(to='catalog.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ShoesPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('images', models.ImageField(default=b'/static/img/shoesimage.jpg', null=True, upload_to=catalog.models.get_file_path, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='shoes',
            name='image',
            field=models.ManyToManyField(to='catalog.ShoesPhotos', blank=True),
        ),
    ]
