from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^index$', views.index_view_pacientes, name='index'),
	url(r'^index_c$', views.index_view_controles, name='index_c'),
	url(r'^$', views.login_view, name='login'),
	url(r'^login$', views.login_view, name='login'),
	url(r'^logout$', views.logout_view, name='logout'),
	url(r'^registro$', views.registro_usuario, name='registro'),
	url(r'^editarperfil$', views.editar_usuario, name='editarperfil'),
	url(r'^verpaciente/(?P<paciente_id>[\w]+)/$', views.verpaciente_view, name='verpaciente'),
	url(r'^ingreso$', views.ingreso_paciente, name='ingreso'),
	url(r'^editarpaciente/(?P<paciente_id>[\w]+)/$', views.editar_paciente, name='editarpaciente'),
	url(r'^verpaciente/(?P<paciente_id>[\w]+)/control$', views.control_view, name='control'),
	url(r'^ajax_dosis$', views.ajax_view_dosis, name='ajax_dosis'),
	url(r'^ajax_inr$', views.ajax_view_inr, name='ajax_inr'),
	url(r'^modal/(?P<control_id>[\w]+)/$', views.ajax_view_modal, name='modal'),
	url(r'^esquema/(?P<control_id>[\w]+)/$', views.ajax_view_esquema, name='mod_esquema'),
	url(r'^vercontrol/(?P<control_id>[\w]+)/$', views.ajax_view_control, name='vercontrol'),
	url(r'^activar/(?P<uid>[\w]+)/$', views.activar_view, name='activar'),
	url(r'^esquema_descargar/(?P<control_id>[\w]+)/$', views.esquema_view, name='esquema'),
	url(r'^pdf$', views.pdf_view, name='pdf')
]
