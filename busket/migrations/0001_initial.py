# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasketModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_user_hash', models.CharField(max_length=200)),
                ('quantity', models.IntegerField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('shoes_id', models.ForeignKey(to='catalog.ShoeSizeParams')),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=100)),
                ('user_phone', models.CharField(max_length=100)),
                ('user_address', models.TextField(max_length=350)),
                ('user_mail', models.EmailField(max_length=100)),
                ('shoes_quantity', models.CharField(max_length=550, null=True, blank=True)),
                ('order_id', models.ManyToManyField(to='catalog.ShoeParameters')),
            ],
        ),
    ]
