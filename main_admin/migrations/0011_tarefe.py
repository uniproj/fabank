# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0010_bill'),
    ]

    operations = [
        migrations.CreateModel(
            name='tarefe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pay', models.IntegerField(default=0)),
            ],
        ),
    ]
