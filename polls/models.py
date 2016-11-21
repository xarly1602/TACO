from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


class Cargo(models.Model):
	cargo_id = models.AutoField(primary_key=True)
	cargo_nombre = models.CharField(max_length=128, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'cargo'
	def __str__(self):
		return self.cargo_nombre


class Ciudad(models.Model):
	ciudad_id = models.AutoField(primary_key=True)
	region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
	ciudad_nombre = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'ciudad'
	def __str__(self):
		return self.ciudad_nombre


class Comuna(models.Model):
	comuna_id = models.AutoField(primary_key=True)
	ciudad = models.ForeignKey('Ciudad', models.DO_NOTHING, blank=True, null=True)
	comuna_nombre = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'comuna'
	def __str__(self):
		return self.comuna_nombre


class Control(models.Model):
	control_id = models.AutoField(primary_key=True)
	paciente = models.ForeignKey('Paciente', models.DO_NOTHING, blank=True, null=True)
	profesional = models.ForeignKey('Profesional', models.DO_NOTHING, blank=True, null=True)
	medicamento = models.ForeignKey('Medicamento', models.DO_NOTHING, blank=True, null=True)
	diagnostico = models.ForeignKey('Diagnostico', models.DO_NOTHING, blank=True, null=True)
	control_fecha = models.DateField(blank=True, null=True)
	control_inr = models.FloatField(blank=True, null=True)
	control_dosis = models.FloatField(blank=True, null=True)
	control_fechasiguiente = models.DateField(blank=True, null=True)
	control_lugar = models.CharField(max_length=512, blank=True, null=True)
	control_inr_p = models.FloatField(blank=True, null=True)
	control_dosis_p = models.FloatField(blank=True, null=True)
	control_evolucion = models.TextField(blank=True, null=True)
	control_estado = models.BooleanField(default=False)

	class Meta:
		managed = True
		db_table = 'control'
	def __str__(self):
		return str(self.paciente.persona.persona_rut) + " - " + str(self.control_fecha)


class Diagnostico(models.Model):
	diagnostico_id = models.AutoField(primary_key=True)
	diagnostico_nombre = models.CharField(max_length=1024, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'diagnostico'
	def __str__(self):
		return self.diagnostico_nombre


class LugarDeTrabajo(models.Model):
	lugar_id = models.AutoField(primary_key=True)
	lugar_nombre = models.CharField(max_length=1024, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'lugar_de_trabajo'
	def __str__(self):
		return self.lugar_nombre


class Medicamento(models.Model):
	medicamento_id = models.AutoField(primary_key=True)
	medicamento_nombre = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'medicamento'
	def __str__(self):
		return self.medicamento_nombre


class Paciente(models.Model):
	persona = models.ForeignKey('Persona', models.DO_NOTHING)
	paciente_id = models.AutoField(primary_key=True)
	plan = models.ForeignKey('Plansalud', models.DO_NOTHING, blank=True, null=True)	
	paciente_nficha = models.IntegerField(blank=True, null=True)
	paciente_telefonoemergencia = models.CharField(max_length=128, blank=True, null=True)
	paciente_anamnesis = models.TextField(blank=True, null=True)
	paciente_rango = models.CharField(max_length=16, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'paciente'
		unique_together = (('persona', 'paciente_id'), ('persona', 'paciente_id'),)
	def __str__(self):
		return self.persona.persona_rut


class PacienteDiagnostico(models.Model):
	paciente_diagnostico_id = models.AutoField(primary_key=True)
	paciente = models.ForeignKey('Paciente', models.DO_NOTHING)
	diagnostico = models.ForeignKey('Diagnostico', models.DO_NOTHING)

	class Meta:
		managed = True
		db_table = 'paciente_diagnostico'
		unique_together = (('paciente', 'diagnostico'), ('paciente', 'diagnostico'),)
	def __str__(self):
		return str(self.paciente.persona.persona_rut) + " - " + str(self.diagnostico.diagnostico_nombre)


class Persona(models.Model):
	user = models.OneToOneField(User, null = True)
	persona_id = models.AutoField(primary_key=True)
	comuna = models.ForeignKey('Comuna', models.DO_NOTHING, blank=True, null=True)
	persona_nombre = models.CharField(max_length=256, blank=True, null=True)
	persona_apellidopaterno = models.CharField(max_length=128, blank=True, null=True)
	persona_apellidomaterno = models.CharField(max_length=128, blank=True, null=True)
	persona_rut = models.CharField(max_length=128, blank=True, null=True)
	persona_sexo = models.IntegerField(blank=True, null=True)
	persona_direccion = models.CharField(max_length=1024, blank=True, null=True)
	persona_telefonocontacto = models.CharField(max_length=128, blank=True, null=True)
	persona_correo = models.CharField(max_length=1024, blank=True, null=True)
	persona_fechanacimiento = models.DateField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'persona'

	def __str__(self):
		return self.persona_rut


class Plansalud(models.Model):
	plan_id = models.AutoField(primary_key=True)
	plan_nombre = models.CharField(max_length=256, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'plansalud'
	def __str__(self):
		return self.plan_nombre


class Profesional(models.Model):
	persona = models.ForeignKey('Persona', models.DO_NOTHING)
	profesional_id = models.AutoField(primary_key=True)
	cargo = models.ForeignKey('Cargo', models.DO_NOTHING, blank=True, null=True)
	profesional_tipo = models.IntegerField(blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'profesional'
		unique_together = (('persona', 'profesional_id'), ('persona', 'profesional_id'),)
	def __str__(self):
		return self.persona.persona_rut


class ProfesionalLugar(models.Model):
	profesional_lugar_id = models.AutoField(primary_key=True)
	lugar = models.ForeignKey('LugarDeTrabajo', models.DO_NOTHING)
	persona = models.ForeignKey('Profesional', models.DO_NOTHING)
	

	class Meta:
		managed = True
		db_table = 'profesional_lugar'
		unique_together = (('lugar', 'persona'), ('lugar', 'persona'),)
	def __str__(self):
		return str(self.persona.persona_rut) + " - " + str(self.lugar.lugar_nombre)


class Region(models.Model):
	region_id = models.AutoField(primary_key=True)
	region_nombre = models.CharField(max_length=1024, blank=True, null=True)

	class Meta:
		managed = True
		db_table = 'region'
	def __str__(self):
		return self.region_nombre
