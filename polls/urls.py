from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index_view, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^registro$', views.registro_usuario, name='registro'),
    url(r'^verpaciente/(?P<paciente_id>[\w]+)/$', views.verpaciente_view, name='verpaciente'),
    url(r'^ingreso$', views.ingreso_paciente, name='ingreso'),
    url(r'^control$', views.control_view, name='control'),
]
