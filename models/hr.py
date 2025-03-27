from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheHR(models.Model):
    _inherit = 'hr.employee'

    certificate = fields.Selection([
        ('basica','Basica'),
        ('media','Media'),
        ('superior','Superior')], 'Nivel de Estudios', default='media')

    afp = fields.Selection([
        ('capital','AFP Capital'),
        ('cuprum','AFP Cuprum'),
        ('habitat','AFP Habitat'),
        ('modelo','AFP Modelo'),
        ('planvital','AFP Planvital'),
        ('provida','AFP Provida'),
        ('uno','AFP Uno')], 'AFP')
    
    salud = fields.Selection([
        ('fonasa','Fonasa'),
        ('banmedica','Banmedica'),
        ('colmena','Colmena'),
        ('consalud','Consalud'),
        ('cruzblanca','Cruz Blanca'),
        ('masvida','Masvida'),
        ('vidatres','Vida Tres')], 'Sistema de Salud')

    caja = fields.Selection([
        ('andes','CCAF Los Andes'),
        ('araucana','CCAF La Araucana'),
        ('heroes','CCAF Los Heroes'),
        ('18','CCAF 18 de Septiembre')], 'Caja de Compensacion')

    sueldo = fields.Integer(string='Base')
    bono_prod = fields.Integer(string='Producción')
    bono_resp = fields.Integer(string='Responsabilidad')
    bono_resp_taller = fields.Integer(string='Responsabilidad Taller')
    bono_comi = fields.Integer(string='Comision Taller')
    bono_punt = fields.Integer(string='Puntualidad')
    bono_asist = fields.Integer(string='Asistencia')
    bono_movil = fields.Integer(string='Movilizacion')
    bono_colac = fields.Integer(string='Colacion')
    bono_estud = fields.Integer(string='Estudio')
    bono_estud_esp = fields.Integer(string='Estudio Especial')
    capac = fields.Html(string='Capacitaciones y/o Cursos')