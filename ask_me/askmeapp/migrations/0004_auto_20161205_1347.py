# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-05 13:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('askmeapp', '0003_question_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('compose_key', models.CharField(default=b'None0', max_length=70, unique=True)),
                ('is_liked', models.BooleanField(default=False)),
                ('is_disliked', models.BooleanField(default=False)),
                ('answer', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='askmeapp.Answer')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='answerlikes',
            field=models.ManyToManyField(to='askmeapp.AnswerLike'),
        ),
    ]
