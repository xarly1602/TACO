# -*- encoding: utf-8 -*-
import datetime, csv
import cStringIO as StringIO
from cgi import escape
from django.shortcuts import render, redirect, render_to_response
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from polls.forms import *
from polls.models import *
from polls.tables import *
from polls.predictor import *
from polls.utilidades import *

@login_required(login_url='login')
def index_view_pacientes(request):
	listarPersonas = PersonaTable()
#	return render_to_pdf("pdf.html", {'pagesize':'A4'})
	return render(request, "index.html", {'listarPersonas': listarPersonas})

@login_required(login_url='login')
def index_view_controles(request):
	print request.user
	persona = Persona.objects.filter(persona_rut=request.user)
	profesional = Profesional.objects.filter(persona=persona)
	print profesional[0].profesional_tipo
	listaControles = IndexControlTable(Control.objects.filter(control_estado = False))
	listaControlesNM = IndexControlTableNoMedico(Control.objects.filter(control_estado = False))
	return render(request, "index_c.html", {'listarPersonas': listaControles, 'listarPersonasNM': listaControlesNM, 'tipo': profesional[0].profesional_tipo})

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

@login_required(login_url='login')
def verpaciente_view(request, paciente_id):
	paciente = Paciente.objects.get(paciente_id = paciente_id)
	controles = Control.objects.filter(paciente=paciente).filter(control_estado = True)
	listaControles = ControlTable(Control.objects.filter(paciente=paciente))
	listaControlesInc = IncControlTable(Control.objects.filter(paciente=paciente))
	rango = paciente.paciente_rango.replace(" ", "").split("-")
	r_min = float(rango[0])
	r_max = float(rango[1])
	inr_list = []
	for c in Control.objects.filter(paciente=paciente):
		inr_list.append(c.control_inr)
	usuario = request.user
	persona = Persona.objects.get(user = usuario)
	profesional = Profesional.objects.get(persona = persona)
	predictor = Predictor(1)
	if request.method == 'POST':
		if True:
			form = FormIniciarControl(request.POST, request.FILES)
			# Comprobamos si el formulario es valido
			if form.is_valid():
				cleaned_data = form.cleaned_data
				fecha = cleaned_data.get('fecha')
				inr = cleaned_data.get('inr')
				[mantener, dias] = Predictor(1).predecir_fecha(inr, r_min, r_max, r_min, r_max, inr_list) #inr, lim_min, lim_max, rto_min, rto_max, inr_list
				dosis = cleaned_data.get('dosis')
				if len(controles) != 0:
					if mantener:
						dosis = controles[len(controles)-1].control_dosis
					else:
						inr = float(inr)				   
						dosis_anterior = controles[len(controles)-1].control_dosis
						curva = predictor.calcula_mejor_curva(dosis_anterior, inr)
						dosis = predictor.calcula_dosis(2.5, curva)
				control = Control()
				control.paciente = Paciente.objects.get(paciente_id=paciente_id)
				control.control_fecha = fecha
				control.control_inr = inr
				controles = Control.objects.filter(paciente=paciente_id)
				if len(controles) >= 3:
					dosis_h = list()
					inr_h = list()
					dosis_h.append(0)
					dosis = float(dosis)
					for control in controles:
						dosis_h.append(control.control_dosis)
						inr_h.append(control.control_inr)
					dosis_h.pop()
					control.control_inr_p =	predictor.predecir_inr(dosis_h, inr_h, dosis)
				if dias not in [-1,0,1]:
					fechasiguiente = fecha + datetime.timedelta(days=dias)
					control.control_fechasiguiente = fechasiguiente
				control.control_dosis = dosis
				control.save()
				print("control")
				messages.success(request, 'Control ingresado con éxito')
				form = FormIniciarControl()
		else:
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
		else:
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
			tipo = cleaned_data.get('tipo_empleado')
			cargo = cleaned_data.get('cargo')
			user_model = User.objects.create_user(username=rut, password=rut)
			user_model.email = correo
			user_model.is_active = False		
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
			profesional = Profesional()
			profesional.persona = persona
			profesional.profesional_tipo = tipo
			profesional.profesional_cargo = cargo
			profesional.save()
			messages.success(request, 'Usuario ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' creado con exito.')
			asunto = "Activar usuario: " + nombre + " " + apellidoPaterno
			uid = user_model.id
			link = "http://127.0.0.1:8000/polls/activar/" + Utilidades().encriptar("TACO_2016", str(uid))
			#mensaje = "Se le informa que el el usuario " + nombre + " " + apellidoPaterno + ", se ha registrado en el sistema TacoSmart.\nEn el siguiente link podrá activar la cuenta del nuevo usuario: \n\n"+link
			send_mail(
				asunto,
				link,
				'admin@tacosmart.cl',
				['xarly1602@gmail.com'],
				fail_silently = False,
			)
			return HttpResponseRedirect(reverse('index'))
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
	profesional = Profesional.objects.get(persona=persona)	
	if request.method == 'POST':
		form = FormEditarUsuario(request.POST, request.FILES)
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
			cargo = cleaned_data.get('cargo') 
			persona.persona_nombre = nombre.lower()
			persona.persona_apellidopaterno = apellidoPaterno.lower()
			persona.persona_apellidomaterno = apellidoMaterno.lower()
			persona.persona_rut = rut.replace(".","").replace("-","")
			persona.persona_sexo = sexo
			persona.persona_direccion = direccion.lower()
			persona.persona_telefonocontacto = telefono
			persona.persona_correo = correo.lower()
			persona.persona_fechanacimiento = fechaNacimiento
			profesional.cargo = cargo
			profesional.save()
			persona.save()
			messages.success(request, 'Usuario ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' editado con exito.')
			return HttpResponseRedirect(reverse('index'))
	else:
		form = FormEditarUsuario(initial={
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
			'cargo': profesional.cargo,
			'pid': profesional.profesional_id
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
			pd.persona = paciente
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
	rto = paciente.paciente_rango.replace(" ", "").split('-')
	rto_min = float(rto[0])
	rto_max = float(rto[1])
	if request.method == 'POST':
		form = FormEditarPaciente(request.POST, request.FILES)
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
			rto_min = cleaned_data.get('rto_min')
			rto_max = cleaned_data.get('rto_max')
			rto = str(rto_min) + " - " + str(rto_max)
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
			paciente.paciente_rango = rto # Rango terapeutico por defecto
			paciente.save()
			messages.success(request, 'Paciente ' + nombre.lower() + ' ' + apellidoPaterno.lower() + ' ' + apellidoMaterno.lower() + ' editado con exito.')			
			return HttpResponseRedirect(reverse('index'))
	else:
		form = FormEditarPaciente(initial={
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
			'anamnesis': paciente.paciente_anamnesis,
			'rto_min': rto_min,
			'rto_max': rto_max
			})
	context = {'form': form}
	return render(request, 'editarpaciente.html', context)

@login_required(login_url='login')
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

@login_required(login_url='login')
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

@login_required(login_url='login')
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
			inr_p = "Faltan datos para la estimación"
			return HttpResponse(inr_p)

@login_required(login_url='login')
def ajax_view_modal(request, paciente_id, control_id):
	usuario = request.user
	persona = Persona.objects.get(user = usuario)
	profesional = Profesional.objects.get(persona = persona)
	paciente = Paciente.objects.get(paciente_id = paciente_id)
	tipo = profesional.profesional_tipo
	if request.method == 'GET':
		print (control_id)
		if tipo == 1 and control_id != '0':
			control = Control.objects.get(control_id=control_id)
			paciente = control.paciente
			form = FormNuevoControl(initial={
				'fecha': control.control_fecha, 
				'inr': control.control_inr, 
				'dosis': control.control_dosis,
				'inr_predicho': control.control_inr_p,
				'siguiente_control': control.control_fechasiguiente,
				'control_id': control.control_id})
			return HttpResponse(render_to_response("ingresarcontrol.html", {'form': form, 'control': control, 'paciente': paciente}, context_instance=RequestContext(request)))
		else:
			form = FormIniciarControl(initial={'fecha': date.today(), 'inr': 0})
			return HttpResponse(render_to_response("ingresarcontrol.html", {'form': form, 'paciente': paciente}, context_instance=RequestContext(request)))
	return render_to_response("ingresarcontrol.html")

@login_required(login_url='login')
def ajax_view_control(request, control_id):
	control = Control.objects.get(control_id=control_id)
	paciente = control.paciente
	if request.method == 'GET':
		return HttpResponse(render_to_response("vercontrol.html", {'paciente': paciente, 'control': control}, context_instance=RequestContext(request)))
	else:
		return render_to_response("vercontrol.html")

@login_required(login_url='login')
def ajax_view_esquema(request, control_id):
	control = Control.objects.get(control_id=control_id)
	esquema = Utilidades().esquemaSemanal(control.control_dosis)
	form = FormEsquema(initial={
		'dia_1':esquema[0],
		'dia_2':esquema[1],
		'dia_3':esquema[2],
		'dia_4':esquema[3],
		'dia_5':esquema[4],
		'dia_6':esquema[5],
		'dia_7':esquema[6],
		})
	if request.method == 'GET':
		return HttpResponse(render_to_response("esquema.html", {'form': form, 'control': control}, context_instance=RequestContext(request)))
	else:
		return render_to_response("esquema.html")

@login_required(login_url='login')
def logout_view(request):
	logout(request)
	messages.success(request, 'Te has desconectado con exito.')
	return redirect(reverse('login'))

@login_required(login_url='login')
def listarPersonas(request):
	listarPersonas = PersonaTable()
	return render(request, "index.html", {'listarPersonas': listarPersonas})

def activar_view(request, uid):
	user_id = Utilidades().desencriptar("TACO_2016", uid)
	user = User.objects.get(id=user_id)
	persona = Persona.objects.get(user=user)
	profesional = Profesional.objects.get(persona=persona)
	if request.method == 'GET':
		form = FormActivarUsuario(initial={
			'rut':persona.persona_rut,
			'nombre':persona.persona_nombre,
			'apellido_paterno':persona.persona_apellidopaterno,
			'apellido_materno':persona.persona_apellidomaterno,
			'direccion':persona.persona_direccion,
			'telefono':persona.persona_telefonocontacto,
			'sexo':persona.persona_sexo,
			'fecha_de_nacimiento':persona.persona_fechanacimiento,
			'correo':persona.persona_correo,
			'tipo_empleado':profesional.profesional_tipo,
			'cargo':profesional.cargo,
			'pid':user.id
			})
		return render(request, "activar.html", {'usuario': user, 'persona': persona, 'form': form})
	else:
		user.is_active = True
		user.save()
		messages.success(request, 'Usuario ' + persona.persona_nombre + ' ' + persona.persona_apellidopaterno + ' activado con exito.')
		return HttpResponseRedirect(reverse('index'))

def handler404(request):
	response = render_to_response('404.html', {},
								  context_instance=RequestContext(request))
	response.status_code = 404
	return response

def handler500(request):
	response = render_to_response('500.html', {},
								  context_instance=RequestContext(request))
	response.status_code = 500
	return response

def esquema_view(request, control_id):
	control = Control.objects.get(control_id=control_id)
	paciente = control.paciente
	diagnostico = PacienteDiagnostico.objects.filter(paciente=paciente)
	esquema = Utilidades().esquemaSemanal(control.control_dosis)
	nombre_archivo = 'Esquema' + control.paciente.persona.persona_rut
	form = FormEsquema(initial={
		'dia_1':esquema[0],
		'dia_2':esquema[1],
		'dia_3':esquema[2],
		'dia_4':esquema[3],
		'dia_5':esquema[4],
		'dia_6':esquema[5],
		'dia_7':esquema[6],
		})
	context = {
		'form': form,
		'esquema': esquema,
		'paciente': paciente,
		'control': control,
		'diagnostico': diagnostico,
	} 
	return render_to_pdf("pdf.html", context)
	#response = HttpResponse(content_type='text/csv')
	#response['Content-Disposition'] = 'attachment; filename="'+nombre_archivo+'.csv"'
	#writer = csv.writer(response)
	#writer.writerow(['Día 1', 'Día 2', 'Día 3', 'Día 4', 'Día 5', 'Día 6', 'Día 7'])
	#writer.writerow(esquema)
	#return response

def pdf_view(request):
	return render_to_pdf("pdf.html", {'pagesize':'A4','mylist': results})

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    #context = Context(context_dict)
    html  = template.render(context_dict)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
