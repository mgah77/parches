from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ParcheCliente(models.Model):
    _inherit = 'res.partner'

    property_payment_term_id = fields.Many2one(default =lambda self: self._default_plazo)

    def _default_plazo(self):
        # Aquí defines la lógica para obtener el valor predeterminado del campo cliente.
        # Por ejemplo, para establecer el cliente con el id 4 ("nomo") como predeterminado:
        plazopago = self.env['account.payment.term'].browse(3)
        return plazopago