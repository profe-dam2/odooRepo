# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class proyectos(models.Model):
#     _name = 'proyectos.proyectos'
#     _description = 'proyectos.proyectos'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


from odoo import models, fields, api, exceptions
from dateutil.relativedelta import *
from datetime import date


class departamento(models.Model):
    _name = 'proyectos.departamento'
    _description = 'Define los atributos de un departamento'

    # Atributos
    nombreDpto = fields.Char(string='Nombre departamento', required=True)

    #Relacion entre tablas
    empleado_id = fields.One2many('proyectos.empleado','departamento_id', string='Departamento')

class empleado(models.Model):
    _name = 'proyectos.empleado'
    _description = 'Define los atributos de un empleado'

    # Atributos
    dniEmpleado = fields.Char(string='DNI', required=True)
    nombreEmpleado = fields.Char(string='Nombre y apellidos', required=True)
    fechaNacimiento = fields.Date(string='Fecha Nacimiento', required=True, default = fields.date.today())
    direccionEmpleado = fields.Char(string='Direccion')
    telefonoEmpleado = fields.Char(string='Telefono')
    edad = fields.Integer('Edad', compute='_getEdad')
    #Relacion de tablas
    departamento_id = fields.Many2one('proyectos.departamento', string='Departamentos')
    proyecto_ids = fields.Many2many('proyectos.proyecto', string='Proyectos')

    @api.depends('fechaNacimiento')
    def _getEdad(self):
        hoy = date.today()
        for empleado in self:
            empleado.edad = relativedelta(hoy, empleado.fechaNacimiento).years

    @api.constrains('dniEmpleado')
    def _checkDNI(self):
        for empleado in self:
            if (len(empleado.dniEmpleado) > 9):
                raise exceptions.ValidationError("El DNI no puede tener mas 9 caracteres")
            if (len(empleado.dniEmpleado) < 9):
                raise exceptions.ValidationError("El DNI no puede tener menos 9 caracteres")


class proyecto(models.Model):
     _name = 'proyectos.proyecto'
     _description = 'Define los atributos de un proyecto'

     #Atributos
     nombreProyecto = fields.Char(string='Nombre proyecto', required=True)
     tipoProyecto = fields.Selection(string='Tipo de proyecto', selection=[('f','Front-End'),('b','Back-End')], help='Tipo de proyecto al que se esta destinando' )
     descripcionProyecto = fields.Text(string='Descripcion del proyecto')
     fechaInicio = fields.Date(string='Fecha de inicio', required=True)
     fechaFin = fields.Date(string='Fecha de fin', required=True)
     #Relacion entre tablas
     empleado_ids = fields.Many2many('proyectos.empleado', string='Empleados')
     
     @api.depends('fechaInicio')
     def _checkFechaInicio(self):
        hoy = date.today()
        for proyecto in self:
            proyecto.fechaInicio
            dias = relativedelta(hoy, proyecto.fechaInicio).days
            if (dias < 0):
                raise exceptions.ValidationError("La fecha no puede ser anterior a hoy")