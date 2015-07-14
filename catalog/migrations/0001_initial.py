# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
import catalog.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
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
            name='ShoeParameters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model_of_shoe', models.CharField(max_length=50, null=True, blank=True)),
                ('color', models.CharField(max_length=50)),
                ('zise', models.CharField(max_length=50)),
                ('date_manufac', models.DateField()),
                ('quantity', models.IntegerField()),
                ('height_shoe', models.CharField(max_length=50, null=True, blank=True)),
                ('height_heel', models.CharField(max_length=50, null=True, blank=True)),
                ('len_of_stelka', models.CharField(max_length=50, null=True, blank=True)),
                ('len_of_feet', models.CharField(max_length=50, null=True, blank=True)),
                ('material', models.CharField(max_length=50, null=True, blank=True)),
                ('vkladka', models.CharField(max_length=50, null=True, blank=True)),
                ('main_image', models.ImageField(default=b'/static/img/shoesimage.jpg', null=True, upload_to=catalog.models.get_file_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('manufacturer', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=150, null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('category_name', models.ManyToManyField(to='catalog.Category')),
                ('relation_to_shoes_params', models.ManyToManyField(to='catalog.ShoeParameters')),
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
            model_name='shoeparameters',
            name='relation_to_shoes_photos',
            field=models.ManyToManyField(to='catalog.ShoesPhotos'),
        ),
    ]
