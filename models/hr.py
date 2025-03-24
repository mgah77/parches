from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheHR(models.Model):
    _inherit = 'hr.employee'

    certificate = fields.Selection([
        ('basica','Basica'),
        ('media','Media'),
        ('superior','Superior')], 'Nivel de Estudios', default='media')

    