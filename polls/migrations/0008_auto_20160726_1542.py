# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-26 15:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

	dependencies = [
		('polls', '0007_auto_20160720_2132'),
	]

	operations = [
		migrations.RenameField(
			model_name='control',
			old_name='control_error',
			new_name='control_dosis_p',
		),
		migrations.AddField(
			model_name='control',
			name='control_estado',
			field=models.BooleanField(default=False),
		),
	]
