# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-04 20:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_check'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.user_account'),
        ),
        migrations.AlterField(
            model_name='check',
            name='dar_vajh',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='check',
            name='user_acc',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main_admin.account'),
        ),
    ]