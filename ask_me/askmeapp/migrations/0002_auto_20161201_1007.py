# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-01 10:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('askmeapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionlike',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
