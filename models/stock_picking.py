from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheStockPicking(models.Model):
    _inherit = 'stock.picking'

    def set_use_document(self):
        return (self.picking_type_id and self.picking_type_id.code != 'incoming') 

    use_documents = fields.Boolean (string = 'Usar Guia de Despacho', default=set_use_document,)