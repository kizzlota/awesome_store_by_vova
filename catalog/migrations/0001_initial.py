# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import catalog.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
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
                ('new_price', models.IntegerField(null=True, blank=True)),
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
            field=models.ManyToManyField(to='catalog.ShoesPhotos'),
        ),
    ]
