# -*- encoding: utf-8 -*- #
from django import forms
from django.contrib.auth.models import User
from polls.models import *
from polls.validators import *
from django.forms.extras.widgets import SelectDateWidget
from datetime import date

class FormRegistroUsuario(forms.Form):
    rut = forms.CharField(min_length=3)
    nombre = forms.CharField(min_length=3)
    apellido_paterno = forms.CharField(min_length=3)
    apellido_materno = forms.CharField(min_length=3)
    direccion = forms.CharField(min_length=3)
    telefono = forms.CharField(min_length=7)
    sexo = forms.ChoiceField(widget=forms.Select, choices=(('0', 'Seleccionar Sexo'), ('1', 'Hombre',), ('2', 'Mujer',)))
    fecha_de_nacimiento = forms.DateField(widget=SelectDateWidget(), required = False)
    correo = forms.EmailField(widget=forms.EmailInput)
    
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

	
		