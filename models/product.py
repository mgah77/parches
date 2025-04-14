from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplateInherit2(models.Model):  # ✅ Nombre de clase personalizado
    _inherit = 'product.template' # ✅ Corrección válida

    @api.multi
    def write(self, vals):
        _logger.info("WRITE personalizado ejecutado para product.template")
        res = super(ProductTemplateInherit2, self).write(vals)
        now = fields.Datetime.now()
        formatted_time = now.strftime('%d/%m/%Y %H:%M:%S')
        for record in self:
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en este producto el <i>%s</i>.") % (self.env.user.name, formatted_time),
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res