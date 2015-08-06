# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
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
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.CharField(default='\u043e\u0431\u0440\u043e\u0431\u043a\u0430', max_length=20, choices=[('\u043e\u0431\u0440\u043e\u0431\u043a\u0430', 'processing'), ('\u0432\u0456\u0434\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e', 'sent'), ('\u0434\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u043e', 'delivered')])),
            ],
        ),
    ]
