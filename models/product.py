from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplateInherit2(models.Model):  
    _inherit = 'product.template'
    _name = False

    @api.multi
    def write(self, vals):
        _logger.info("WRITE personalizado ejecutado para product.template")
        res = super(ProductTemplateInherit2, self).write(vals)
        for record in self:
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en este producto.") % self.env.user.name,
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res