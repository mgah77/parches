from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = ['product.template', 'mail.thread']

    @api.multi
    def write(self, vals):
        _logger.info("WRITE personalizado ejecutado para product.template")
        res = super(ProductTemplate, self).write(vals)
        for record in self:
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en este producto.") % self.env.user.name,
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res