# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestShoes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TestShoesParams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('color', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TestShoesPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='testshoesparams',
            name='relation_to_photos',
            field=models.ManyToManyField(to='testing_issues.TestShoesPhotos'),
        ),
        migrations.AddField(
            model_name='testshoes',
            name='relation_to_test',
            field=models.ManyToManyField(to='testing_issues.TestShoesParams'),
        ),
    ]
