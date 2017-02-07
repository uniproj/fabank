# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20170205_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='vam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField(default=0)),
                ('monthes', models.IntegerField(default=0)),
                ('payed', models.IntegerField(default=0)),
                ('payback', models.IntegerField(default=0)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user_account')),
            ],
        ),
    ]
