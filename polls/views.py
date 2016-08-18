# -*- encoding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from polls.forms import *
from polls.models import *
from polls.tables import *
from polls.predictor import *

@login_required(login_url='login')
def index_view(request):
	listarPersonas = PersonaTable()
	return render(request, "index.html", {'listarPersonas': listarPersonas})

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
	listaControlesInc = IncControlTable(Control.objects.filter(paciente=paciente).filter(control_estado = False))
	paciente = Paciente.objects.get(paciente_id = paciente_id)
	usuario = request.user
	persona = Persona.objects.get(user = usuario)
	profesional = Profesional.objects.get(persona = persona)
	if request.method == 'POST':
		if profesional.profesional_tipo == 0:
			form = FormIniciarControl(request.POST, request.FILES)
			# Comprobamos si el formulario es valido
			if form.is_valid():
				cleaned_data = form.cleaned_data
				fecha = cleaned_data.get('fecha')
				inr = cleaned_data.get('inr')
				dosis = cleaned_data.get('dosis')
				control = Control()
				control.paciente = Paciente.objects.get(paciente_id=paciente_id)
				control.control_fecha = fecha
				control.control_inr = inr
				control.control_dosis = dosis
				control.save()
				print("control")
				messages.success(request, 'Control ingresado con éxito')
				form = FormIniciarControl()
		elif profesional.profesional_tipo == 1:
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
				evolucion = cleaned_data.get('evolucion')
				control_id = cleaned_data.get('control_id')
				control = Control.objects.get(control_id=control_id)
				control.paciente = paciente
				control.profesional = profesional
				control.medicamento = medicamento
				control.control_fecha = fecha
				control.control_inr = inr
				control.control_dosis = dosis
				control.control_fechasiguiente = fechasiguiente
				control.control_lugar = lugar
				control.control_evolucion = evolucion
				control.control_estado = True
				control.save()
				messages.success(request, 'Control guardado con éxito')
				form = FormNuevoControl()
		return HttpResponseRedirect(reverse('verpaciente', kwargs={'paciente_id': paciente_id}))
	else:
		if profesional.profesional_tipo == 0:
			form = FormIniciarControl(initial={'fecha': date.today(), 'inr': 0, 'dosis': 0})
		elif profesional.profesional_tipo == 1:
			form = FormNuevoControl(initial={'fecha': date.today(), 'inr': 0, 'dosis': 0})
	return render(request, 'verpaciente.html', {
		'form': form, 
		'paciente': paciente, 
		'listaControles': listaControles, 
		'profesional': profesional,
		'listaControlesInc': listaControlesInc
		})

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
def editar_usuario(request):
	usuario = request.user
	persona = Persona.objects.get(user=usuario)
	pid = persona.persona_id
	p = Persona.objects.get(persona_id = pid)
	profesional = Profesional.objects.get(persona=p)
	persona = profesional.persona
	if request.method == 'POST':
		form = FormRegistroUsuario(request.POST, request.FILES)
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
			tipo = cleaned_data.get('tipo') 
			persona.persona_nombre = nombre.lower()
			persona.persona_apellidopaterno = apellidoPaterno.lower()
			persona.persona_apellidomaterno = apellidoMaterno.lower()
			persona.persona_rut = rut.replace(".","").replace("-","")
			persona.persona_sexo = sexo
			persona.persona_direccion = direccion.lower()
			persona.persona_telefonocontacto = telefono
			persona.persona_correo = correo.lower()
			persona.persona_fechanacimiento = fechaNacimiento
			profesional.profesional_tipo = tipo
			profesional.save()
			persona.save()
			messages.success(request, 'Usuario ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' creado con exito.')
			return HttpResponseRedirect(reverse('index'))
	else:
		form = FormRegistroUsuario(initial={
			'rut': persona.persona_rut,
			'nombre': persona.persona_nombre,
			'apellido_paterno': persona.persona_apellidopaterno,
			'apellido_materno': persona.persona_apellidomaterno,
			'direccion': persona.persona_direccion,
			'telefono': persona.persona_telefonocontacto,
			'sexo': persona.persona_sexo,
			'fecha_de_nacimiento': persona.persona_fechanacimiento,
			'correo': persona.persona_correo,
			'tipo_empleado': profesional.profesional_tipo,
			'cargo': profesional.cargo
			})
	context = {'form': form}
	return render(request, 'editarusuario.html', context)

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
            diagnostico = cleaned_data.get('diagnostico')
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
            pd = PacienteDiagnostico()
            pd.paciente = paciente
            pd.diagnostico = diagnostico
            pd.save()
            messages.success(request, 'Paciente ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' ingresado con exito.')
            form = FormRegistroPaciente()
            return HttpResponseRedirect(reverse('index'))
    else:
        form = FormRegistroPaciente()
    context = {'form': form}
    return render(request, 'ingreso.html', context)

@login_required(login_url='login')
def editar_paciente(request, paciente_id):
	paciente = Paciente.objects.get(paciente_id=paciente_id)
	persona = paciente.persona
	if request.method == 'POST':
		form = FormRegistroPaciente(request.POST, request.FILES)
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
			#diagnostico = cleaned_data.get('diagnostico')
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
			return HttpResponseRedirect(reverse('index'))
	else:
		form = FormRegistroPaciente(initial={
			'rut': persona.persona_rut,
			'numero_de_ficha': paciente.paciente_nficha,
			'nombre': persona.persona_nombre,
			'apellido_paterno': persona.persona_apellidopaterno,
			'apellido_materno': persona.persona_apellidomaterno,		
			'direccion': persona.persona_direccion,
			'telefono_de_contacto': persona.persona_telefonocontacto,
			'sexo': persona.persona_sexo,
			'fecha_de_nacimiento': persona.persona_fechanacimiento,
			'plan_de_salud': paciente.plan,
			'anamnesis': paciente.paciente_anamnesis
			})
	context = {'form': form}
	return render(request, 'editarpaciente.html', context)

def control_view(request, paciente_id):
    paciente = Paciente.objects.get(paciente_id = paciente_id)
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
            evolucion = cleaned_data.get('evolucion')
            control = Control()
            control.paciente = Paciente.objects.get(paciente_id=paciente_id)
            control.medicamento = medicamento
            control.control_fecha = fecha
            control.control_inr = inr
            control.control_dosis = dosis
            control.control_fechasiguiente = fechasiguiente
            control.control_lugar = lugar
            control.control_evolucion = evolucion
            control.save()
            messages.success(request, 'Control guardado con éxito')
            form = FormNuevoControl()
            return HttpResponseRedirect(reverse('verpaciente', kwargs={'paciente_id': paciente_id}))
    else:
        form = FormNuevoControl(initial={'fecha': date.today(), 'inr': 0})
    context = {
        'form': form,
        'paciente': paciente
    }
    return render(request, 'control.html', context)

def ajax_view_dosis(request):
    if request.method == 'GET':
        paciente_id = request.GET['id_paciente']
        inr = request.GET['inr']        
        predictor = Predictor(0)
        controles = Control.objects.filter(paciente=paciente_id)                
        if len(inr) != 0 and len(controles) != 0:
            inr = float(inr)                   
            dosis_anterior = controles[len(controles)-1].control_dosis
            curva = predictor.calcula_mejor_curva(dosis_anterior, inr)
            dosis = predictor.calcula_dosis(2.5, curva)
            return HttpResponse(dosis)
        else:
            dosis = 0 
            return HttpResponse(dosis)

def ajax_view_inr(request):
    if request.method == 'GET':
        paciente_id = request.GET['id_paciente']
        dosis = request.GET['dosis']
        predictor = Predictor(1)
        controles = Control.objects.filter(paciente=paciente_id)
        if len(controles) >= 3:
            dosis_h = list()
            inr = list()
            dosis_h.append(0)
            dosis = float(dosis)
            for control in controles:
                dosis_h.append(control.control_dosis)
                inr.append(control.control_inr)
            x = dosis_h.pop()
            inr_p = predictor.predecir_inr(dosis_h, inr, dosis)
            return HttpResponse(inr_p)
        else:
            inr_p = "Faltan datos para la predicción"
            return HttpResponse(inr_p)

def ajax_view_modal(request, control_id):
    usuario = request.user
    persona = Persona.objects.get(user = usuario)
    profesional = Profesional.objects.get(persona = persona)
    tipo = profesional.profesional_tipo
    if request.method == 'GET':
        if tipo == 1:
            control = Control.objects.get(control_id=control_id)
            paciente = control.paciente
            form = FormNuevoControl(initial={
                'fecha': control.control_fecha, 
                'inr': control.control_inr, 
                'dosis': control.control_dosis,
                'inr_predicho': control.control_inr_p,
                'control_id': control.control_id})
            return HttpResponse(render_to_response("ingresarcontrol.html", {'form': form, 'control': control, 'paciente': paciente}, context_instance=RequestContext(request)))
        elif tipo == 0:
            form = FormIniciarControl(initial={'fecha': date.today(), 'inr': 0, 'dosis': 0})
            return HttpResponse(render_to_response("ingresarcontrol.html", {'form': form}, context_instance=RequestContext(request)))
    return render_to_response("ingresarcontrol.html")

def ajax_view_control(request, control_id):
	control = Control.objects.get(control_id=control_id)
	paciente = control.paciente
	if request.method == 'GET':
		return HttpResponse(render_to_response("vercontrol.html", {'paciente': paciente, 'control': control}, context_instance=RequestContext(request)))
	else:
		return render_to_response("vercontrol.html")

def logout_view(request):
    logout(request)
    messages.success(request, 'Te has desconectado con exito.')
    return redirect(reverse('login'))

def listarPersonas(request):
    listarPersonas = PersonaTable()
    return render(request, "index.html", {'listarPersonas': listarPersonas})

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response