# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-17 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker', '0012_auto_20171117_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_start',
            field=models.BooleanField(default=False),
        ),
    ]
