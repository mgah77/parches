from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheCliente(models.Model):
    _inherit = 'res.partner'

    company_type = fields.Selection(selection=[('company','Company'),('person','Individual')])