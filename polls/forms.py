# -*- encoding: utf-8 -*- #
from django import forms
from django.contrib.auth.models import User
from polls.models import *
from polls.validators import *
from django.forms.extras.widgets import SelectDateWidget
from django.forms.widgets import NumberInput
from datetime import date

class FormRegistroUsuario(forms.Form):
    rut = forms.CharField(min_length=3)
    nombre = forms.CharField(min_length=3)
    apellido_paterno = forms.CharField(min_length=3)
    apellido_materno = forms.CharField(min_length=3)
    direccion = forms.CharField(min_length=3)
    telefono = forms.CharField(min_length=7)
    sexo = forms.ChoiceField(widget=forms.Select, choices=(('0', 'Seleccionar Sexo'), ('1', 'Hombre',), ('2', 'Mujer',)))
    fecha_de_nacimiento = forms.DateField(widget=SelectDateWidget(years=range(1980, date.today().year+1)), required = False)
    correo = forms.EmailField(widget=forms.EmailInput)
    tipo_empleado = forms.ChoiceField(widget=forms.Select, choices=(('', 'Seleccionar tipo de empleado'), ('0', 'No médico',), ('1', 'Médico',)))
    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), empty_label="Seleccione cargo", to_field_name="cargo_nombre", required=False)
    
    def clean_rut(self):        
        rut = self.cleaned_data['rut']
        if not Validators().rutValido(rut):
            raise forms.ValidationError('El rut no es válido.')
        if Persona.objects.filter(persona_rut=rut):
            raise forms.ValidationError('El rut ingresado ya se encuentra registrado.')
        return rut

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        for letra in nombre:
            if letra.isdigit():
                raise forms.ValidationError('El nombre no debe contener números')
        return nombre

    def clean_apellido_paterno(self):
        apellido = self.cleaned_data['apellido_paterno']
        for letra in apellido:
            if letra.isdigit():
                raise forms.ValidationError('El apellido no debe contener números')
        return apellido

    def clean_apellido_materno(self):
        apellido = self.cleaned_data['apellido_materno']
        for letra in apellido:
            if letra.isdigit():
                raise forms.ValidationError('El apellido no debe contener números')
        return apellido

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        for digito in telefono:
            if not digito.isdigit():
                raise forms.ValidationError('El número de teléfono no debe contener letras')
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if Persona.objects.filter(persona_correo=correo):
            raise forms.ValidationError('Ya existe un correo igual en la db.')
        return correo

    def clean_sexo(self):
        sexo = self.cleaned_data['sexo']
        if sexo == '0':
            raise forms.ValidationError('Por favor seleccione el sexo de la persona')
        return sexo

    def clean_fecha_de_nacimiento(self):
        fecha = self.cleaned_data['fecha_de_nacimiento']
        print fecha
        if fecha != None and fecha > date.today():
            raise forms.ValidationError('Ingrese una fecha válida')
        return fecha

class FormRegistroPaciente(forms.Form):
    rut = forms.CharField(min_length=3)
    numero_de_ficha = forms.IntegerField()
    nombre = forms.CharField(min_length=3)
    apellido_paterno = forms.CharField(min_length=3)
    apellido_materno = forms.CharField(min_length=3)
    diagnostico = forms.ModelChoiceField(queryset=Diagnostico.objects.all(), empty_label="Seleccione diagnostico", to_field_name="diagnostico_nombre", required=False)
    direccion = forms.CharField(min_length=3)
    telefono_de_contacto = forms.CharField(min_length=7)
    sexo = forms.ChoiceField(widget=forms.Select, choices=(('0', 'Seleccionar Sexo'), ('1', 'Hombre',), ('2', 'Mujer',)))
    fecha_de_nacimiento = forms.DateField(widget=SelectDateWidget(years=range(1960, date.today().year+1)), required = False)
    #correo = forms.EmailField(widget=forms.EmailInput, required = False)
    plan_de_salud = forms.ModelChoiceField(queryset=Plansalud.objects.all(), empty_label="Seleccione Plan de Salud", to_field_name="plan_nombre")
    anamnesis = forms.CharField(widget=forms.Textarea)
    def clean_rut(self):        
        rut = self.cleaned_data['rut']
        if not Validators().rutValido(rut):
            raise forms.ValidationError('El rut no es válido.')
        if Persona.objects.filter(persona_rut=rut):
            raise forms.ValidationError('El rut ingresado ya se encuentra registrado.')
        return rut

    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        for letra in nombre:
            if letra.isdigit():
                raise forms.ValidationError('El nombre no debe contener números')
        return nombre

    def clean_apellido_paterno(self):
        apellido = self.cleaned_data['apellido_paterno']
        for letra in apellido:
            if letra.isdigit():
                raise forms.ValidationError('El apellido no debe contener números')
        return apellido

    def clean_apellido_materno(self):
        apellido = self.cleaned_data['apellido_materno']
        for letra in apellido:
            if letra.isdigit():
                raise forms.ValidationError('El apellido no debe contener números')
        return apellido

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        for digito in telefono:
            if not digito.isdigit():
                raise forms.ValidationError('El número de teléfono no debe contener letras')
        return telefono

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if correo != "" and Persona.objects.filter(persona_correo=correo):
            raise forms.ValidationError('Ya existe un correo igual en la db.')
        return correo

    def clean_sexo(self):
        sexo = self.cleaned_data['sexo']
        if sexo == '0':
            raise forms.ValidationError('Por favor seleccione el sexo de la persona')
        return sexo

    def clean_fecha_de_nacimiento(self):
        fecha = self.cleaned_data['fecha_de_nacimiento']
        print fecha
        if fecha != None and fecha > date.today():
            raise forms.ValidationError('Ingrese una fecha válida')
        return fecha

class FormIniciarControl(forms.Form):
    fecha = forms.DateField(widget=SelectDateWidget(years=range(1960, date.today().year+1)), required = True)
    inr = forms.FloatField(min_value=0, max_value=10,widget=NumberInput(attrs={'type': 'number', 'step': "0.1"}))
    dosis = forms.FloatField(min_value=0)
    def clean_fecha(self):
        fechaC = self.cleaned_data['fecha']        
        if fechaC != None and fechaC > date.today():
            raise forms.ValidationError('Ingrese una fecha válida')
        return fechaC

class FormNuevoControl(forms.Form):
    #paciente = models.ForeignKey('Paciente', models.DO_NOTHING, blank=True, null=True)
    #persona = models.ForeignKey('Profesional', models.DO_NOTHING, blank=True, null=True)
    medicamento = forms.ModelChoiceField(queryset=Medicamento.objects.all(), empty_label="Seleccione Medicamento", to_field_name="medicamento_nombre")
    fecha = forms.DateField(widget=SelectDateWidget(years=range(1960, date.today().year+1)), required = True)
    inr = forms.FloatField(min_value=0, max_value=10,widget=NumberInput(attrs={'type': 'number', 'step': "0.1"}))
    dosis = forms.FloatField(min_value=0)
    inr_predicho = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}), required = False)
    siguiente_control = forms.DateField(widget=SelectDateWidget(years=range(1960, date.today().year+1)), required = False)
    lugar = forms.CharField(min_length=3)
    evolucion = forms.CharField(widget=forms.Textarea)
    control_id = forms.CharField(required=False, widget=forms.HiddenInput())

    def clean_fecha(self):
        fechaC = self.cleaned_data['fecha']        
        if fechaC != None and fechaC > date.today():
            raise forms.ValidationError('Ingrese una fecha válida')
        return fechaC

    def clean_inr(self):
        inrC = self.cleaned_data['inr']        
        if inrC != None and inrC <= 0:
            raise forms.ValidationError('El valor del INR no es válido')
        return inrC

    def clean_dosis(self):
        dosisC = self.cleaned_data['dosis']        
        if dosisC != None and dosisC <= 0:
            raise forms.ValidationError('El valor de la dosis no es válido')
        return dosisC

    def clean_siguiente_control(self):
        siguienteC = self.cleaned_data['siguiente_control']        
        if siguienteC == None or siguienteC <= date.today():
            raise forms.ValidationError('Ingrese una fecha válida')
        return siguienteC