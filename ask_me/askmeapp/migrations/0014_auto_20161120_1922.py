# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-20 19:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askmeapp', '0013_auto_20161120_1418'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='tag',
            new_name='tags',
        ),
    ]