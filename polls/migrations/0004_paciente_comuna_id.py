# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-16 21:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20160516_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='paciente',
            name='comuna_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
