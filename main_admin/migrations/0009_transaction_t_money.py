# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0008_auto_20170205_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='t_money',
            field=models.IntegerField(default=0),
        ),
    ]
