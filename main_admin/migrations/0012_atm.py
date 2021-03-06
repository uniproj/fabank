# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-05 22:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_admin', '0011_tarefe'),
    ]

    operations = [
        migrations.CreateModel(
            name='ATM',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_1000', models.IntegerField(default=0)),
                ('a_2000', models.IntegerField(default=0)),
                ('a_5000', models.IntegerField(default=0)),
                ('a_10000', models.IntegerField(default=0)),
                ('a_50000', models.IntegerField(default=0)),
                ('acc', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_admin.account')),
                ('bch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_admin.branch')),
            ],
        ),
    ]
