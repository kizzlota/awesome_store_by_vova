# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='decription',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='shoes',
            name='image',
            field=models.ImageField(default=b'/static/img/shoesimage.jpg', null=True, upload_to=b'shoes_images', blank=True),
        ),
    ]
