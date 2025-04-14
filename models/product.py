from odoo import models, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductTemplateInherit2(models.Model): 
    _inherit = 'product.template'

    @api.multi
    def write(self, vals):
        _logger.info("WRITE personalizado ejecutado para product.template")
        res = super(ProductTemplateInherit2, self).write(vals)
        for record in self:
            modified_fields = ', '.join([field for field in vals.keys()])
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en los siguientes campos: <b>%s</b>") % (
                    self.env.user.name, modified_fields),
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res