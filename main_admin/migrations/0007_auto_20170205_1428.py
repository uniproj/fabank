# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0006_auto_20170205_1417'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='t_time',
        ),
        migrations.AlterField(
            model_name='transaction',
            name='t_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
