# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askmeapp', '0011_auto_20161120_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(default=b'General', max_length=50, verbose_name='\u041a\u0430\u0442\u0435\u0433\u043e\u0440\u0438\u044f'),
        ),
    ]
