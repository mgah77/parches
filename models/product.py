from odoo import models, api, _
import Datetime
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = False  # Muy importante para evitar conflictos

    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        now = fields.Datetime.now()
        formatted_time = now.strftime('%d/%m/%Y %H:%M:%S')  # Formato de fecha y hora
        for record in self:
            modified_fields = ', '.join([field for field in vals.keys()])  # Nombres de los campos modificados
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en los siguientes campos el <i>%s</i>: <b>%s</b>") % (
                    self.env.user.name, formatted_time, modified_fields),
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res