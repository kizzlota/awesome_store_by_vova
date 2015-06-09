# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150529_1738'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoes',
            old_name='decription',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description',
        ),
        migrations.AddField(
            model_name='shoes',
            name='date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
