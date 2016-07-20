from __future__ import unicode_literals

from django.db import models


class Cargo(models.Model):
    cargo_id = models.AutoField(primary_key=True)
    cargo_nombre = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargo'


class Ciudad(models.Model):
    ciudad_id = models.AutoField(primary_key=True)
    region = models.ForeignKey('Region', models.DO_NOTHING, blank=True, null=True)
    ciudad_nombre = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ciudad'


class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    ciudad = models.ForeignKey(Ciudad, models.DO_NOTHING, blank=True, null=True)
    comuna_nombre = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comuna'


class Control(models.Model):
    control_id = models.AutoField(primary_key=True)
    persona = models.ForeignKey('Paciente', models.DO_NOTHING)
    paciente_id = models.IntegerField()
    pro_persona = models.ForeignKey('Profesional', models.DO_NOTHING)
    profesional_id = models.IntegerField()
    diagnostico = models.ForeignKey('Diagnostico', models.DO_NOTHING, blank=True, null=True)
    medicamento = models.ForeignKey('Medicamento', models.DO_NOTHING, blank=True, null=True)
    control_fecha = models.DateField(blank=True, null=True)
    control_inr = models.FloatField(blank=True, null=True)
    control_dosis = models.FloatField(blank=True, null=True)
    control_fechasiguiente = models.DateField(blank=True, null=True)
    control_lugar = models.CharField(max_length=512, blank=True, null=True)
    control_inr_p = models.FloatField(blank=True, null=True)
    control_error = models.FloatField(blank=True, null=True)
    control_evolucion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'control'


class Diagnostico(models.Model):
    diagnostico_id = models.AutoField(primary_key=True)
    diagnostico_nombre = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnostico'


class LugarDeTrabajo(models.Model):
    lugar_id = models.AutoField(primary_key=True)
    lugar_nombre = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lugar_de_trabajo'


class Medicamento(models.Model):
    medicamento_id = models.AutoField(primary_key=True)
    medicamento_nombre = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medicamento'


class Paciente(models.Model):
    persona = models.ForeignKey('Persona', models.DO_NOTHING)
    paciente_id = models.AutoField()
    plan = models.ForeignKey('Plansalud', models.DO_NOTHING, blank=True, null=True)
    comuna_id = models.IntegerField(blank=True, null=True)
    persona_nombre = models.CharField(max_length=256, blank=True, null=True)
    persona_apellidopaterno = models.CharField(max_length=128, blank=True, null=True)
    persona_apellidomaterno = models.CharField(max_length=128, blank=True, null=True)
    persona_rut = models.CharField(max_length=128, blank=True, null=True)
    persona_sexo = models.IntegerField(blank=True, null=True)
    persona_direccion = models.CharField(max_length=1024, blank=True, null=True)
    persona_telefonocontacto = models.CharField(max_length=128, blank=True, null=True)
    persona_correo = models.CharField(max_length=1024, blank=True, null=True)
    persona_fechanacimiento = models.DateField(blank=True, null=True)
    paciente_nficha = models.IntegerField(blank=True, null=True)
    paciente_telefonoemergencia = models.CharField(max_length=128, blank=True, null=True)
    paciente_anamnesis = models.TextField(blank=True, null=True)
    paciente_rango = models.CharField(max_length=16, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paciente'
        unique_together = (('persona', 'paciente_id'), ('persona', 'paciente_id'),)


class PacienteDiagnostico(models.Model):
    persona = models.ForeignKey(Paciente, models.DO_NOTHING)
    paciente_id = models.IntegerField()
    diagnostico = models.ForeignKey(Diagnostico, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paciente_diagnostico'
        unique_together = (('persona', 'paciente_id', 'diagnostico'), ('persona', 'paciente_id', 'diagnostico'),)


class Persona(models.Model):
    persona_id = models.AutoField(primary_key=True)
    comuna = models.ForeignKey(Comuna, models.DO_NOTHING, blank=True, null=True)
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
        managed = False
        db_table = 'persona'


class Plansalud(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_nombre = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plansalud'


class Profesional(models.Model):
    persona = models.ForeignKey(Persona, models.DO_NOTHING)
    profesional_id = models.AutoField()
    cargo = models.ForeignKey(Cargo, models.DO_NOTHING, blank=True, null=True)
    comuna_id = models.IntegerField(blank=True, null=True)
    persona_nombre = models.CharField(max_length=256, blank=True, null=True)
    persona_apellidopaterno = models.CharField(max_length=128, blank=True, null=True)
    persona_apellidomaterno = models.CharField(max_length=128, blank=True, null=True)
    persona_rut = models.CharField(max_length=128, blank=True, null=True)
    persona_sexo = models.IntegerField(blank=True, null=True)
    persona_direccion = models.CharField(max_length=1024, blank=True, null=True)
    persona_telefonocontacto = models.CharField(max_length=128, blank=True, null=True)
    persona_correo = models.CharField(max_length=1024, blank=True, null=True)
    persona_fechanacimiento = models.DateField(blank=True, null=True)
    profesional_tipo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profesional'
        unique_together = (('persona', 'profesional_id'), ('persona', 'profesional_id'),)


class ProfesionalLugar(models.Model):
    lugar = models.ForeignKey(LugarDeTrabajo, models.DO_NOTHING)
    persona = models.ForeignKey(Profesional, models.DO_NOTHING)
    profesional_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'profesional_lugar'
        unique_together = (('lugar', 'persona', 'profesional_id'), ('lugar', 'persona', 'profesional_id'),)


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_nombre = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'region'
