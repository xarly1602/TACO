from polls.models import Persona
from polls.models import Paciente
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
	persona_nombre = Column(field='persona.persona_nombre', header=u'Nombre')
	persona_apellidopaterno = Column(field='persona.persona_apellidopaterno', header=u'Apellido Paterno')
	persona_apellidomaterno = Column(field='persona.persona_apellidomaterno', header=u'Apellido Materno')
	#persona_rut = Column(field='persona_rut', header=u'Rut')
	#persona_sexo = Column(field='persona_sexo', header=u'Sexo')
	#persona_direccion = Column(field='persona_direccion', header=u'Direccion')
	#persona_telefonocontacto = Column(field='persona_telefonocontacto', header=u'Telefono')
	#persona_correo =Column(field='persona_correo', header=u'Correo')
	#persona_fechanacimiento = Column(field='persona_fechanacimiento', header=u'Fecha de Nacimiento')
	persona = Column(field='persona.persona_fechanacimiento', header=u'F de Nacimiento')
	#paciente_id = Column(field='paciente_id', header=u'Id')
	plan =  Column(field='plan.plan_nombre', header=u'Plan')   
	paciente_nficha = Column(field='paciente_nficha', header=u'Numero de ficha')
	#paciente_telefonoemergencia = Column(field='paciente_telefonoemergencia', header=u'Numero de contacto')
	#paciente_anamnesis = Column(header=u'Anamnesis')
	name = LinkColumn(header=u'NAME', links=[
        Link(viewname='verpaciente', args=(A('paciente_id'),), text='ver')])
        #Link(viewname='temp', args=(A('paciente_id'),), text=A('paciente_nombre'))])
	class Meta:
		model = Paciente
		#unique_together = (('persona', 'paciente_id'), ('persona', 'paciente_id'),)
        
		