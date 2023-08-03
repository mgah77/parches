from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheCliente(models.Model):
    _inherit = 'res.partner'

    property_payment_term_id = fields.Many2one(required=True, default=lambda self: self._default_plazo())

    def _default_plazo(self):
        plazos = self.env['account.payment.term'].search([], limit=1)
        return plazos