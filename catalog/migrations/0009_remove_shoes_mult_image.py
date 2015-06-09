# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20150603_1711'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoes',
            name='mult_image',
        ),
    ]
