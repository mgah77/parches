from odoo import models, api, _
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = ['product.template', 'mail.thread']
   
 
    @api.multi
    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        for record in self:
            user_name = self.env.user.name
            record.message_post(
                body=_("El usuario <b>%s</b> realizó cambios en este producto.") % user_name,
                message_type="notification",
                subtype="mail.mt_note"
            )
        return res