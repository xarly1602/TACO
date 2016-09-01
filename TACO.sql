/*==============================================================*/
/* DBMS name:	  PostgreSQL 8								 */
/* Created on:	 20-07-2016 16:47:05						  */
/*==============================================================*/


drop index CARGO_PK;

drop table CARGO;

drop index RELATIONSHIP_3_FK;

drop index CIUDAD_PK;

drop table CIUDAD;

drop index RELATIONSHIP_4_FK;

drop index COMUNA_PK;

drop table COMUNA;

drop index RELATIONSHIP_15_FK;

drop index RELATIONSHIP_10_FK;

drop index RELATIONSHIP_9_FK;

drop index RELATIONSHIP_8_FK;

drop index CONTROL_PK;

drop table CONTROL;

drop index DIAGNOSTICO_PK;

drop table DIAGNOSTICO;

drop index LUGAR_DE_TRABAJO_PK;

drop table LUGAR_DE_TRABAJO;

drop index MEDICAMENTO_PK;

drop table MEDICAMENTO;

drop index INHERITANCE_2_FK;

drop index RELATIONSHIP_1_FK;

drop index PACIENTE_PK;

drop table PACIENTE;

drop index RELATIONSHIP_14_FK;

drop index RELATIONSHIP_13_FK;

drop index RELATIONSHIP_12_PK;

drop table PACIENTE_DIAGNOSTICO;

drop index RELATIONSHIP_5_FK;

drop index PERSONA_PK;

drop table PERSONA;

drop index PLANSALUD_PK;

drop table PLANSALUD;

drop index INHERITANCE_1_FK;

drop index RELATIONSHIP_2_FK;

drop index PROFESIONAL_PK;

drop table PROFESIONAL;

drop index RELATIONSHIP_12_FK;

drop index RELATIONSHIP_11_FK;

drop index RELATIONSHIP_11_PK;

drop table PROFESIONAL_LUGAR;

drop index REGION_PK;

drop table REGION;

/*==============================================================*/
/* Table: CARGO												 */
/*==============================================================*/
create table CARGO (
   CARGO_ID			 SERIAL			   not null,
   CARGO_NOMBRE		 VARCHAR(128)		 null,
   constraint PK_CARGO primary key (CARGO_ID)
);

/*==============================================================*/
/* Index: CARGO_PK											  */
/*==============================================================*/
create unique index CARGO_PK on CARGO (
CARGO_ID
);

/*==============================================================*/
/* Table: CIUDAD												*/
/*==============================================================*/
create table CIUDAD (
   CIUDAD_ID			SERIAL			   not null,
   REGION_ID			INT4				 null,
   CIUDAD_NOMBRE		VARCHAR(256)		 null,
   constraint PK_CIUDAD primary key (CIUDAD_ID)
);

/*==============================================================*/
/* Index: CIUDAD_PK											 */
/*==============================================================*/
create unique index CIUDAD_PK on CIUDAD (
CIUDAD_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_3_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_3_FK on CIUDAD (
REGION_ID
);

/*==============================================================*/
/* Table: COMUNA												*/
/*==============================================================*/
create table COMUNA (
   COMUNA_ID			SERIAL			   not null,
   CIUDAD_ID			INT4				 null,
   COMUNA_NOMBRE		VARCHAR(256)		 null,
   constraint PK_COMUNA primary key (COMUNA_ID)
);

/*==============================================================*/
/* Index: COMUNA_PK											 */
/*==============================================================*/
create unique index COMUNA_PK on COMUNA (
COMUNA_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_4_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_4_FK on COMUNA (
CIUDAD_ID
);

/*==============================================================*/
/* Table: CONTROL											   */
/*==============================================================*/
create table CONTROL (
   CONTROL_ID		   SERIAL			   not null,
   PERSONA_ID		   INT4				 not null,
   PACIENTE_ID		  INT4				 not null,
   PRO_PERSONA_ID	   INT4				 not null,
   PROFESIONAL_ID	   INT4				 not null,
   DIAGNOSTICO_ID	   INT4				 null,
   MEDICAMENTO_ID	   INT4				 null,
   CONTROL_FECHA		DATE				 null,
   CONTROL_INR		  FLOAT8			   null,
   CONTROL_DOSIS		FLOAT8			   null,
   CONTROL_FECHASIGUIENTE DATE				 null,
   CONTROL_LUGAR		VARCHAR(512)		 null,
   CONTROL_INR_P		FLOAT8			   null,
   CONTROL_ERROR		FLOAT8			   null,
   CONTROL_EVOLUCION	TEXT				 null,
   constraint PK_CONTROL primary key (CONTROL_ID)
);

/*==============================================================*/
/* Index: CONTROL_PK											*/
/*==============================================================*/
create unique index CONTROL_PK on CONTROL (
CONTROL_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_8_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_8_FK on CONTROL (
PRO_PERSONA_ID,
PROFESIONAL_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_9_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_9_FK on CONTROL (
MEDICAMENTO_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_10_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_10_FK on CONTROL (
PERSONA_ID,
PACIENTE_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_15_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_15_FK on CONTROL (
DIAGNOSTICO_ID
);

/*==============================================================*/
/* Table: DIAGNOSTICO										   */
/*==============================================================*/
create table DIAGNOSTICO (
   DIAGNOSTICO_ID	   SERIAL			   not null,
   DIAGNOSTICO_NOMBRE   VARCHAR(1024)		null,
   constraint PK_DIAGNOSTICO primary key (DIAGNOSTICO_ID)
);

/*==============================================================*/
/* Index: DIAGNOSTICO_PK										*/
/*==============================================================*/
create unique index DIAGNOSTICO_PK on DIAGNOSTICO (
DIAGNOSTICO_ID
);

/*==============================================================*/
/* Table: LUGAR_DE_TRABAJO									  */
/*==============================================================*/
create table LUGAR_DE_TRABAJO (
   LUGAR_ID			 SERIAL			   not null,
   LUGAR_NOMBRE		 VARCHAR(1024)		null,
   constraint PK_LUGAR_DE_TRABAJO primary key (LUGAR_ID)
);

/*==============================================================*/
/* Index: LUGAR_DE_TRABAJO_PK								   */
/*==============================================================*/
create unique index LUGAR_DE_TRABAJO_PK on LUGAR_DE_TRABAJO (
LUGAR_ID
);

/*==============================================================*/
/* Table: MEDICAMENTO										   */
/*==============================================================*/
create table MEDICAMENTO (
   MEDICAMENTO_ID	   SERIAL			   not null,
   MEDICAMENTO_NOMBRE   VARCHAR(256)		 null,
   constraint PK_MEDICAMENTO primary key (MEDICAMENTO_ID)
);

/*==============================================================*/
/* Index: MEDICAMENTO_PK										*/
/*==============================================================*/
create unique index MEDICAMENTO_PK on MEDICAMENTO (
MEDICAMENTO_ID
);

/*==============================================================*/
/* Table: PACIENTE											  */
/*==============================================================*/
create table PACIENTE (
   PERSONA_ID		   INT4				 not null,
   PACIENTE_ID		  SERIAL			   not null,
   PLAN_ID			  INT4				 null,
   COMUNA_ID			INT4				 null,
   PERSONA_NOMBRE	   VARCHAR(256)		 null,
   PERSONA_APELLIDOPATERNO VARCHAR(128)		 null,
   PERSONA_APELLIDOMATERNO VARCHAR(128)		 null,
   PERSONA_RUT		  VARCHAR(128)		 null,
   PERSONA_SEXO		 INT4				 null,
   PERSONA_DIRECCION	VARCHAR(1024)		null,
   PERSONA_TELEFONOCONTACTO VARCHAR(128)		 null,
   PERSONA_CORREO	   VARCHAR(1024)		null,
   PERSONA_FECHANACIMIENTO DATE				 null,
   PACIENTE_NFICHA	  INT4				 null,
   PACIENTE_TELEFONOEMERGENCIA VARCHAR(128)		 null,
   PACIENTE_ANAMNESIS   TEXT				 null,
   PACIENTE_RANGO	   VARCHAR(16)		  null,
   constraint PK_PACIENTE primary key (PERSONA_ID, PACIENTE_ID)
);

/*==============================================================*/
/* Index: PACIENTE_PK										   */
/*==============================================================*/
create unique index PACIENTE_PK on PACIENTE (
PERSONA_ID,
PACIENTE_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_1_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_1_FK on PACIENTE (
PLAN_ID
);

/*==============================================================*/
/* Index: INHERITANCE_2_FK									  */
/*==============================================================*/
create  index INHERITANCE_2_FK on PACIENTE (
PERSONA_ID
);

/*==============================================================*/
/* Table: PACIENTE_DIAGNOSTICO								  */
/*==============================================================*/
create table PACIENTE_DIAGNOSTICO (
   PERSONA_ID		   INT4				 not null,
   PACIENTE_ID		  INT4				 not null,
   DIAGNOSTICO_ID	   INT4				 not null,
   constraint PK_PACIENTE_DIAGNOSTICO primary key (PERSONA_ID, PACIENTE_ID, DIAGNOSTICO_ID)
);

/*==============================================================*/
/* Index: RELATIONSHIP_12_PK									*/
/*==============================================================*/
create unique index RELATIONSHIP_12_PK on PACIENTE_DIAGNOSTICO (
PERSONA_ID,
PACIENTE_ID,
DIAGNOSTICO_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_13_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_13_FK on PACIENTE_DIAGNOSTICO (
PERSONA_ID,
PACIENTE_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_14_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_14_FK on PACIENTE_DIAGNOSTICO (
DIAGNOSTICO_ID
);

/*==============================================================*/
/* Table: PERSONA											   */
/*==============================================================*/
create table PERSONA (
   PERSONA_ID		   SERIAL			   not null,
   COMUNA_ID			INT4				 null,
   PERSONA_NOMBRE	   VARCHAR(256)		 null,
   PERSONA_APELLIDOPATERNO VARCHAR(128)		 null,
   PERSONA_APELLIDOMATERNO VARCHAR(128)		 null,
   PERSONA_RUT		  VARCHAR(128)		 null,
   PERSONA_SEXO		 INT4				 null,
   PERSONA_DIRECCION	VARCHAR(1024)		null,
   PERSONA_TELEFONOCONTACTO VARCHAR(128)		 null,
   PERSONA_CORREO	   VARCHAR(1024)		null,
   PERSONA_FECHANACIMIENTO DATE				 null,
   constraint PK_PERSONA primary key (PERSONA_ID)
);

/*==============================================================*/
/* Index: PERSONA_PK											*/
/*==============================================================*/
create unique index PERSONA_PK on PERSONA (
PERSONA_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_5_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_5_FK on PERSONA (
COMUNA_ID
);

/*==============================================================*/
/* Table: PLANSALUD											 */
/*==============================================================*/
create table PLANSALUD (
   PLAN_ID			  SERIAL			   not null,
   PLAN_NOMBRE		  VARCHAR(256)		 null,
   constraint PK_PLANSALUD primary key (PLAN_ID)
);

/*==============================================================*/
/* Index: PLANSALUD_PK										  */
/*==============================================================*/
create unique index PLANSALUD_PK on PLANSALUD (
PLAN_ID
);

/*==============================================================*/
/* Table: PROFESIONAL										   */
/*==============================================================*/
create table PROFESIONAL (
   PERSONA_ID		   INT4				 not null,
   PROFESIONAL_ID	   SERIAL			   not null,
   CARGO_ID			 INT4				 null,
   COMUNA_ID			INT4				 null,
   PERSONA_NOMBRE	   VARCHAR(256)		 null,
   PERSONA_APELLIDOPATERNO VARCHAR(128)		 null,
   PERSONA_APELLIDOMATERNO VARCHAR(128)		 null,
   PERSONA_RUT		  VARCHAR(128)		 null,
   PERSONA_SEXO		 INT4				 null,
   PERSONA_DIRECCION	VARCHAR(1024)		null,
   PERSONA_TELEFONOCONTACTO VARCHAR(128)		 null,
   PERSONA_CORREO	   VARCHAR(1024)		null,
   PERSONA_FECHANACIMIENTO DATE				 null,
   PROFESIONAL_TIPO	 INT4				 null,
   constraint PK_PROFESIONAL primary key (PERSONA_ID, PROFESIONAL_ID)
);

/*==============================================================*/
/* Index: PROFESIONAL_PK										*/
/*==============================================================*/
create unique index PROFESIONAL_PK on PROFESIONAL (
PERSONA_ID,
PROFESIONAL_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_2_FK									 */
/*==============================================================*/
create  index RELATIONSHIP_2_FK on PROFESIONAL (
CARGO_ID
);

/*==============================================================*/
/* Index: INHERITANCE_1_FK									  */
/*==============================================================*/
create  index INHERITANCE_1_FK on PROFESIONAL (
PERSONA_ID
);

/*==============================================================*/
/* Table: PROFESIONAL_LUGAR									 */
/*==============================================================*/
create table PROFESIONAL_LUGAR (
   LUGAR_ID			 INT4				 not null,
   PERSONA_ID		   INT4				 not null,
   PROFESIONAL_ID	   INT4				 not null,
   constraint PK_PROFESIONAL_LUGAR primary key (LUGAR_ID, PERSONA_ID, PROFESIONAL_ID)
);

/*==============================================================*/
/* Index: RELATIONSHIP_11_PK									*/
/*==============================================================*/
create unique index RELATIONSHIP_11_PK on PROFESIONAL_LUGAR (
LUGAR_ID,
PERSONA_ID,
PROFESIONAL_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_11_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_11_FK on PROFESIONAL_LUGAR (
LUGAR_ID
);

/*==============================================================*/
/* Index: RELATIONSHIP_12_FK									*/
/*==============================================================*/
create  index RELATIONSHIP_12_FK on PROFESIONAL_LUGAR (
PERSONA_ID,
PROFESIONAL_ID
);

/*==============================================================*/
/* Table: REGION												*/
/*==============================================================*/
create table REGION (
   REGION_ID			SERIAL			   not null,
   REGION_NOMBRE		VARCHAR(256)		 null,
   constraint PK_REGION primary key (REGION_ID)
);

/*==============================================================*/
/* Index: REGION_PK											 */
/*==============================================================*/
create unique index REGION_PK on REGION (
REGION_ID
);

alter table CIUDAD
   add constraint FK_CIUDAD_RELATIONS_REGION foreign key (REGION_ID)
	  references REGION (REGION_ID)
	  on delete restrict on update restrict;

alter table COMUNA
   add constraint FK_COMUNA_RELATIONS_CIUDAD foreign key (CIUDAD_ID)
	  references CIUDAD (CIUDAD_ID)
	  on delete restrict on update restrict;

alter table CONTROL
   add constraint FK_CONTROL_RELATIONS_PACIENTE foreign key (PERSONA_ID, PACIENTE_ID)
	  references PACIENTE (PERSONA_ID, PACIENTE_ID)
	  on delete restrict on update restrict;

alter table CONTROL
   add constraint FK_CONTROL_RELATIONS_DIAGNOST foreign key (DIAGNOSTICO_ID)
	  references DIAGNOSTICO (DIAGNOSTICO_ID)
	  on delete restrict on update restrict;

alter table CONTROL
   add constraint FK_CONTROL_RELATIONS_PROFESIO foreign key (PRO_PERSONA_ID, PROFESIONAL_ID)
	  references PROFESIONAL (PERSONA_ID, PROFESIONAL_ID)
	  on delete restrict on update restrict;

alter table CONTROL
   add constraint FK_CONTROL_RELATIONS_MEDICAME foreign key (MEDICAMENTO_ID)
	  references MEDICAMENTO (MEDICAMENTO_ID)
	  on delete restrict on update restrict;

alter table PACIENTE
   add constraint FK_PACIENTE_INHERITAN_PERSONA foreign key (PERSONA_ID)
	  references PERSONA (PERSONA_ID)
	  on delete restrict on update restrict;

alter table PACIENTE
   add constraint FK_PACIENTE_RELATIONS_PLANSALU foreign key (PLAN_ID)
	  references PLANSALUD (PLAN_ID)
	  on delete restrict on update restrict;

alter table PACIENTE_DIAGNOSTICO
   add constraint FK_PACIENTE_RELATIONS_PACIENTE foreign key (PERSONA_ID, PACIENTE_ID)
	  references PACIENTE (PERSONA_ID, PACIENTE_ID)
	  on delete restrict on update restrict;

alter table PACIENTE_DIAGNOSTICO
   add constraint FK_PACIENTE_RELATIONS_DIAGNOST foreign key (DIAGNOSTICO_ID)
	  references DIAGNOSTICO (DIAGNOSTICO_ID)
	  on delete restrict on update restrict;

alter table PERSONA
   add constraint FK_PERSONA_RELATIONS_COMUNA foreign key (COMUNA_ID)
	  references COMUNA (COMUNA_ID)
	  on delete restrict on update restrict;

alter table PROFESIONAL
   add constraint FK_PROFESIO_INHERITAN_PERSONA foreign key (PERSONA_ID)
	  references PERSONA (PERSONA_ID)
	  on delete restrict on update restrict;

alter table PROFESIONAL
   add constraint FK_PROFESIO_RELATIONS_CARGO foreign key (CARGO_ID)
	  references CARGO (CARGO_ID)
	  on delete restrict on update restrict;

alter table PROFESIONAL_LUGAR
   add constraint FK_PROFESIO_RELATIONS_LUGAR_DE foreign key (LUGAR_ID)
	  references LUGAR_DE_TRABAJO (LUGAR_ID)
	  on delete restrict on update restrict;

alter table PROFESIONAL_LUGAR
   add constraint FK_PROFESIO_RELATIONS_PROFESIO foreign key (PERSONA_ID, PROFESIONAL_ID)
	  references PROFESIONAL (PERSONA_ID, PROFESIONAL_ID)
	  on delete restrict on update restrict;

