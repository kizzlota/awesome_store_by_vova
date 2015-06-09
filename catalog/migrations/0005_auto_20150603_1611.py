# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_shoes_new_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoes',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
