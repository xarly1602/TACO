# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from polls.models import *

def index (request):
	return HttpResponse("Hola, no se que es esto!.")

@login_required(login_url='login')
def index_view(request):
    return render(request, 'index.html')

def login_view(request):
    # Si el usuario esta ya logueado, lo redireccionamos a index_view
    if request.user.is_authenticated():
        return redirect(reverse('index'))
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                # Redireccionar informando que la cuenta esta inactiva
                # Lo dejo como ejercicio al lector :)
                pass
        mensaje = 'Nombre de usuario o contraseña no valido'
    return render(request, 'login.html', {'mensaje': mensaje})

def registro_usuario(request):
    if request.method == 'POST':
        form = FormRegistroUsuario(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            cleaned_data = form.cleaned_data
            rut = cleaned_data.get('rut').replace('.','').replace('-','')
            nombre = cleaned_data.get('nombre')
            apellidoPaterno = cleaned_data.get('apellido_paterno')
            apellidoMaterno = cleaned_data.get('apellido_materno')
            direccion = cleaned_data.get('direccion')
            telefono = cleaned_data.get('telefono')
            sexo = cleaned_data.get('sexo')
            fechaNacimiento = cleaned_data.get('fecha_de_nacimiento')
            correo = cleaned_data.get('correo')
            user_model = User.objects.create_user(username=rut, password=rut)
            user_model.email = correo            
            persona = Persona()
            persona.persona_nombre = nombre.lower()
            persona.persona_apellidopaterno = apellidoPaterno.lower()
            persona.persona_apellidomaterno = apellidoMaterno.lower()
            persona.persona_rut = rut.replace(".","").replace("-","")
            persona.persona_sexo = sexo
            persona.persona_direccion = direccion.lower()
            persona.persona_telefonocontacto = telefono
            persona.persona_correo = correo.lower()
            persona.persona_fechanacimiento = fechaNacimiento
            persona.user = user_model
            user_model.save()
            persona.save()
            messages.success(request, 'Usuario ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' creado con exito.')
            form = FormRegistroUsuario()
    else:
        form = FormRegistroUsuario()
    context = {
        'form': form
    }
    return render(request, 'registro.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return redirect(reverse('login'))