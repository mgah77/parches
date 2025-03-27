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

    sueldo = fields.Integer()
    bono_prod = fields.Integer()
    