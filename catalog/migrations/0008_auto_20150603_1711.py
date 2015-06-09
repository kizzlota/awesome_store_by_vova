# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20150603_1630'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestMode0l',
        ),
        migrations.AddField(
            model_name='shoes',
            name='mult_image',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
