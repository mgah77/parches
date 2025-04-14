from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = ['product.template', 'mail.thread']
    _name = 'product.template'
    
    @api.multi
    def write(self, vals):
        message = "Producto modificado por %s" % self.env.user.name
        self.message_post(body=message)
        return super(ProductTemplate, self).write(vals)