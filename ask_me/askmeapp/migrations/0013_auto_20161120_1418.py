# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askmeapp', '0012_auto_20161120_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='\u0420\u044d\u0439\u0442\u0438\u043d\u0433'),
        ),
    ]