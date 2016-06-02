from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^index$', views.index_view, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^registro$', views.registro_usuario, name='registro'),
]
