# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20150603_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoes',
            name='new_price',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
