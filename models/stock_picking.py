from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheStockPicking(models.Model):
    _inherit = 'stock.picking'

    use_documents = fields.Boolean (string = 'Usar Guia de Despacho', default=set_use_document,)