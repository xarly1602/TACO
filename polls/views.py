# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from polls.models import *
from polls.tables import *

def index (request):
	return HttpResponse("Hola, no se que es esto!.")

@login_required(login_url='login')
def index_view(request):
    listarPersonas = PersonaTable()
    return render(request, "index.html", {'listarPersonas': listarPersonas})
    #return render(request, 'index.html')

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

def verpaciente_view(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id = paciente_id)
    listaControles = ControlTable(Control.objects.filter(paciente=paciente))
    return render(request, 'verpaciente.html', {'paciente': paciente, 'listaControles': listaControles})

@login_required(login_url='login')
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

@login_required(login_url='login')
def ingreso_paciente(request):
    if request.method == 'POST':
        form = FormRegistroPaciente(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            cleaned_data = form.cleaned_data
            rut = cleaned_data.get('rut').replace('.','').replace('-','')
            ficha = cleaned_data.get('numero_de_ficha')
            nombre = cleaned_data.get('nombre')
            apellidoPaterno = cleaned_data.get('apellido_paterno')
            apellidoMaterno = cleaned_data.get('apellido_materno')
            direccion = cleaned_data.get('direccion')
            telefono = cleaned_data.get('telefono_de_contacto')
            sexo = cleaned_data.get('sexo')
            fechaNacimiento = cleaned_data.get('fecha_de_nacimiento')
            #correo = cleaned_data.get('correo')
            plan = cleaned_data.get('plan_de_salud')
            anamnesis = cleaned_data.get('anamnesis')
            persona = Persona()
            paciente = Paciente()
            persona.persona_nombre = nombre.lower()
            persona.persona_apellidopaterno = apellidoPaterno.lower()
            persona.persona_apellidomaterno = apellidoMaterno.lower()
            persona.persona_rut = rut.replace(".","").replace("-","")
            persona.persona_sexo = sexo
            persona.persona_direccion = direccion.lower()
            persona.persona_telefonocontacto = telefono
            #persona.persona_correo = correo.lower()
            persona.persona_fechanacimiento = fechaNacimiento
            persona.save()
            paciente.persona = persona
            paciente.paciente_anamnesis = anamnesis
            paciente.paciente_nficha = ficha
            paciente.paciente_telefonoemergencia = telefono
            paciente.plan = plan
            paciente.paciente_rango = "2 - 3" # Rango terapeutico por defecto
            paciente.save()
            messages.success(request, 'Paciente ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' ingresado con exito.')
            form = FormRegistroPaciente()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = FormRegistroPaciente()
    context = {
        'form': form
    }
    return render(request, 'ingreso.html', context)

def control_view(request, paciente_id):
    if request.method == 'POST':
        form = FormNuevoControl(request.POST, request.FILES)
        # Comprobamos si el formulario es valido
        if form.is_valid():
            cleaned_data = form.cleaned_data
            medicamento = cleaned_data.get('medicamento')
            fecha = cleaned_data.get('fecha')
            inr = cleaned_data.get('inr')
            dosis = cleaned_data.get('dosis')
            fechasiguiente = cleaned_data.get('siguiente_control')
            lugar = cleaned_data.get('lugar')
            control = Control()
            control.paciente = Paciente.objects.get(paciente_id=paciente_id)
            control.medicamento = medicamento
            control.control_fecha = fecha
            control.control_inr = inr
            control.control_dosis = dosis
            control.control_fechasiguiente = fechasiguiente
            control.control_lugar = lugar
            control.save()
            messages.success(request, 'Control guardado con éxito')
            form = FormNuevoControl()
            return HttpResponseRedirect(reverse('verpaciente', kwargs={'paciente_id': paciente_id}))
    else:
        form = FormNuevoControl(initial={'fecha': date.today()})
    context = {
        'form': form
    }
    return render(request, 'control.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return redirect(reverse('login'))

def listarPersonas(request):
    listarPersonas = PersonaTable()
    return render(request, "index.html", {'listarPersonas': listarPersonas})