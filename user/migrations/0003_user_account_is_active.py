# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-04 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20170131_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_account',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
