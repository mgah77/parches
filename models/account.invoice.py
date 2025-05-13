from odoo import models, fields, api, _

class AccountInvoiceCustom(models.Model):
    _inherit = 'account.invoice'

    def _invoice_lines(self):
        invoice_lines = []
        no_product = False
        MntExe = 0
        currency_base = self.currency_base()
        currency_id = self.currency_target()
        taxInclude = self.document_class_id.es_boleta()
        self._onchange_invoice_line_ids()
        for line in self.with_context(lang="es_CL").invoice_line_ids:
            if not line.account_id:
                continue
            if line.product_id.default_code == "NO_PRODUCT":
                no_product = True
            lines = {}
            lines["NroLinDet"] = line.sequence
            if line.product_id.default_code and not no_product:
                lines["CdgItem"] = {}
                lines["CdgItem"]["TpoCodigo"] = "INT1"
                lines["CdgItem"]["VlrCodigo"] = line.product_id.default_code
            details = line.get_tax_detail()
            lines["Impuesto"] = details['impuestos']
            MntExe += details['MntExe']
            if not taxInclude:
                taxInclude = details['taxInclude']
            if details.get('cod_imp_adic'):
                lines['CodImpAdic'] = details['cod_imp_adic']
            if details.get('IndExe'):
                lines['IndExe'] = details['IndExe']
            # if line.product_id.type == 'events':
            #   lines['ItemEspectaculo'] =
            #            if self._es_boleta():
            #                lines['RUTMandante']
            lines["NmbItem"] = self._acortar_str(line.product_id.name, 80)  #
            lines["DscItem"] = self._acortar_str(line.name, 1000)  # descripción más extenza
            if line.product_id.default_code:
                lines["NmbItem"] = self._acortar_str(
                    line.product_id.name.replace("[" + line.product_id.default_code + "] ", ""), 80
                )
            # lines['InfoTicket']
            qty = round(line.quantity, 4)
            if not no_product:
                lines["QtyItem"] = qty
            if qty == 0 and not no_product:
                lines["QtyItem"] = 1
            elif qty < 0:
                raise UserError("NO puede ser menor que 0")
            if not no_product:
                uom_name = line.uom_id.with_context(exportacion=self.document_class_id.es_exportacion()).name_get()
                lines["UnmdItem"] = uom_name[0][1][:4]
                lines["PrcItem"] = round(line.price_unit, 6)
                if currency_id:
                    lines["OtrMnda"] = {}
                    lines["OtrMnda"]["PrcOtrMon"] = round(
                        currency_base._convert(
                            line.price_unit, currency_id, self.company_id, self.date_invoice, round=False
                        ),
                        4,
                    )
                    lines["OtrMnda"]["Moneda"] = self._acortar_str(currency_id.name, 3)
                    lines["OtrMnda"]["FctConv"] = round(currency_id.rate, 4)
            if line.discount > 0:
                lines["DescuentoPct"] = line.discount
                DescMonto = line.discount_amount
                lines["DescuentoMonto"] = DescMonto
                if currency_id:
                    lines["DescuentoMonto"] = currency_base._convert(
                        DescMonto, currency_id, self.company_id, self.date_invoice
                    )
                    lines["OtrMnda"]["DctoOtrMnda"] = DescMonto
            if line.discount < 0:
                lines["RecargoPct"] = line.discount * -1
                RecargoMonto = line.discount_amount * -1
                lines["RecargoMonto"] = RecargoMonto
                if currency_id:
                    lines["OtrMnda"]["RecargoOtrMnda"] = currency_base._convert(
                        RecargoMonto, currency_id, self.company_id, self.date_invoice
                    )
            if not no_product and not taxInclude:
                price_subtotal = line.price_subtotal
                if currency_id:
                    lines["OtrMnda"]["MontoItemOtrMnda"] = currency_base._convert(
                        price_subtotal, currency_id, self.company_id, self.date_invoice
                    )
                lines["MontoItem"] = price_subtotal
            elif not no_product:
                price_total = line.price_total
                if currency_id:
                    lines["OtrMnda"]["MontoItemOtrMnda"] = currency_base._convert(
                        price_total, currency_id, self.company_id, self.date_invoice
                    )
                lines["MontoItem"] = price_total
            if no_product:
                lines["MontoItem"] = 0
            #if lines["MontoItem"] < 0:
            #   raise UserError(_("No pueden ir valores negativos en las líneas de detalle"))
            if lines.get("PrcItem", 1) == 0:
                del lines["PrcItem"]
            invoice_lines.append(lines)
            if "IndExe" in lines:
                taxInclude = False
        return {
            "Detalle": invoice_lines,
            "MntExe": MntExe,
            "no_product": no_product,
            "tax_include": taxInclude,
        }