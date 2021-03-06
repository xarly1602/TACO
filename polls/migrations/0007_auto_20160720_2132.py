# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-20 21:32
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

	dependencies = [
		('polls', '0006_persona_user'),
	]

	operations = [
		migrations.CreateModel(
			name='Diagnostico',
			fields=[
				('diagnostico_id', models.AutoField(primary_key=True, serialize=False)),
				('diagnostico_nombre', models.CharField(blank=True, max_length=1024, null=True)),
			],
			options={
				'db_table': 'diagnostico',
				'managed': True,
			},
		),
		migrations.CreateModel(
			name='LugarDeTrabajo',
			fields=[
				('lugar_id', models.AutoField(primary_key=True, serialize=False)),
				('lugar_nombre', models.CharField(blank=True, max_length=1024, null=True)),
			],
			options={
				'db_table': 'lugar_de_trabajo',
				'managed': True,
			},
		),
		migrations.CreateModel(
			name='PacienteDiagnostico',
			fields=[
				('paciente_diagnostico_id', models.AutoField(primary_key=True, serialize=False)),
				('diagnostico', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls.Diagnostico')),
			],
			options={
				'db_table': 'paciente_diagnostico',
				'managed': True,
			},
		),
		migrations.CreateModel(
			name='ProfesionalLugar',
			fields=[
				('profesional_lugar_id', models.AutoField(primary_key=True, serialize=False)),
				('lugar', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls.LugarDeTrabajo')),
				('persona', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls.Profesional')),
			],
			options={
				'db_table': 'profesional_lugar',
				'managed': True,
			},
		),
		migrations.RenameField(
			model_name='control',
			old_name='persona',
			new_name='profesional',
		),
		migrations.AddField(
			model_name='control',
			name='control_error',
			field=models.FloatField(blank=True, null=True),
		),
		migrations.AddField(
			model_name='control',
			name='control_evolucion',
			field=models.TextField(blank=True, null=True),
		),
		migrations.AddField(
			model_name='control',
			name='control_inr_p',
			field=models.FloatField(blank=True, null=True),
		),
		migrations.AddField(
			model_name='paciente',
			name='paciente_rango',
			field=models.CharField(blank=True, max_length=16, null=True),
		),
		migrations.AlterField(
			model_name='ciudad',
			name='ciudad_nombre',
			field=models.CharField(blank=True, max_length=256, null=True),
		),
		migrations.AlterField(
			model_name='persona',
			name='user',
			field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
		),
		migrations.AddField(
			model_name='pacientediagnostico',
			name='persona',
			field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='polls.Paciente'),
		),
		migrations.AddField(
			model_name='control',
			name='diagnostico',
			field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='polls.Diagnostico'),
		),
		migrations.AlterUniqueTogether(
			name='profesionallugar',
			unique_together=set([('lugar', 'persona')]),
		),
		migrations.AlterUniqueTogether(
			name='pacientediagnostico',
			unique_together=set([('persona', 'diagnostico')]),
		),
	]
