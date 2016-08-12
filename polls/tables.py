# -*- encoding: utf-8 -*- #
from polls.models import Persona, Paciente, Control, PacienteDiagnostico
from datetime import date
from table import Table
from table.utils import A
from table.columns import Column
from django.core.urlresolvers import reverse_lazy
from table.columns.calendarcolumn import CalendarColumn
from table.columns.sequencecolumn import SequenceColumn
from table.columns.linkcolumn import LinkColumn, Link, ImageLink
from table.columns.checkboxcolumn import CheckboxColumn

class PersonaTable(Table):
	#persona_id = Column(field='persona_id', header=u'Id')
	persona_rut = Column(field='paciente.persona.persona_rut', header=u'Rut')
	persona_nombre = Column(field='paciente.persona.persona_nombre', header=u'Nombre')
	persona_apellidopaterno = Column(field='paciente.persona.persona_apellidopaterno', header=u'Apellido Paterno')
	persona_apellidomaterno = Column(field='paciente.persona.persona_apellidomaterno', header=u'Apellido Materno')
	#persona_sexo = Column(field='persona_sexo', header=u'Sexo')
	#persona_direccion = Column(field='persona_direccion', header=u'Direccion')
	#persona_telefonocontacto = Column(field='persona_telefonocontacto', header=u'Telefono')
	#persona_correo =Column(field='persona_correo', header=u'Correo')
	#persona_fechanacimiento = Column(field='persona_fechanacimiento', header=u'Fecha de Nacimiento')
	#persona = Column(field='persona.persona_fechanacimiento', header=u'F de Nacimiento')
	#paciente_id = Column(field='paciente_id', header=u'Id')
	#plan =  Column(field='plan.plan_nombre', header=u'Plan')   
	diagnostico = Column(field='diagnostico.diagnostico_nombre', header=u'Diagnóstico')
    #paciente_nficha = Column(field='paciente_nficha', header=u'Numero de ficha')
	#paciente_telefonoemergencia = Column(field='paciente_telefonoemergencia', header=u'Numero de contacto')
	#paciente_anamnesis = Column(header=u'Anamnesis')
	name = LinkColumn(header=u'Ver paciente', links=[
        Link(viewname='editarpaciente', args=(A('paciente.paciente_id'),), attrs={'class': 'detalle fa fa-pencil btn'}, text=''),
        Link(viewname='verpaciente', args=(A('paciente.paciente_id'),), attrs={'class': 'detalle fa fa-search btn'}, text='')])
        #Link(viewname='temp', args=(A('paciente_id'),), text=A('paciente_nombre'))])
	class Meta:
		model = PacienteDiagnostico
		#unique_together = (('persona', 'paciente_id'), ('persona', 'paciente_id'),)
        
class ControlTable(Table):
	#paciente = Column()
    #persona = Column()
    control_fecha = Column(field='control_fecha', header=u'Fecha Control')
    #medicamento = Column(field='medicamento.medicamento_nombre', header=u'Medicamento')
    control_inr = Column(field='control_inr', header=u'INR')
    control_dosis = Column(field='control_dosis', header=u'Dosis')
    #control_fechasiguiente = Column() 
    #control_lugar = Column(field='control_lugar', header=u'Lugar')
    name = LinkColumn(header=u'Ver detalle', links=[
        Link(viewname='vercontrol', args=(A('control_id'),), attrs={'class': 'detalle fa fa-search btn', 'data-toggle': 'modal', 'data-target': '#modal'}, text='')])
    class Meta:
    	model = Control

class IncControlTable(Table):
	#paciente = Column()
    #persona = Column()
    control_fecha = Column(field='control_fecha', header=u'Fecha Control')
    #medicamento = Column(field='medicamento.medicamento_nombre', header=u'Medicamento')
    control_inr = Column(field='control_inr', header=u'INR')
    control_dosis = Column(field='control_dosis', header=u'Dosis')
    #control_fechasiguiente = Column() 
    #control_lugar = Column(field='control_lugar', header=u'Lugar')
    name = LinkColumn(header=u'Ingresar control', links=[
        Link(viewname='control', args=(A('paciente_id'),), attrs={'class': 'detalle fa fa-pencil btn'}, text=''),
		Link(viewname='modal', args=(A('control_id'),), attrs={'class': 'detalle fa fa-search btn', 'data-toggle': 'modal', 'data-target': '#modal'}, text='')])    
    class Meta:
    	model = Control