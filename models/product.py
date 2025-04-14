from odoo import models, api, _
import Datetime
import logging
from odoo.tools.safe_eval import safe_eval

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = False  # necesario para que funcione la herencia sin redefinir el modelo

    @api.multi
    def write(self, vals):
        changes = {}
        for record in self:
            for field, new_value in vals.items():
                if field in record._fields:
                    old_value = record[field]
                    # Transforma valores complejos (many2one, etc.) a algo legible
                    if isinstance(old_value, models.BaseModel):
                        old_value = old_value.name
                    if isinstance(new_value, (tuple, list)) and len(new_value) > 0:
                        try:
                            new_value = self.env[record._fields[field].comodel_name].browse(new_value[0]).name
                        except:
                            new_value = str(new_value)
                    changes[field] = {'old': old_value, 'new': new_value}

        res = super(ProductTemplate, self).write(vals)

        if changes:
            now = fields.Datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            for record in self:
                lines = [f"<b>{field}</b>: <i>{data['old']}</i> → <i>{data['new']}</i>" for field, data in changes.items()]
                message = _(
                    "El usuario <b>%s</b> realizó cambios en este producto el <i>%s</i>:<br/>%s"
                ) % (self.env.user.name, now, "<br/>".join(lines))

                record.message_post(
                    body=message,
                    message_type="notification",
                    subtype="mail.mt_note"
                )
        return res