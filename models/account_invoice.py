from odoo import models

class AccountInvoiceParche(models.Model):
    _inherit = 'account.invoice'

    def _invoice_lines(self):
        # Copia IDÉNTICA de la función original, pero sin las 2 líneas comentadas
        invoice_lines = []
        product = True
        MntExe = 0
        MontoNF = 0
        currency_base = self.currency_base()
        currency_id = self.currency_target()
        taxInclude = self.document_class_id.es_boleta()
        
        if self.env["account.invoice.line"].with_context(lang="es_CL").search([
            "|", ("sequence", "=", -1), 
            ("sequence", "=", 0), 
            ("invoice_id", "=", self.id)
        ]):
            self._onchange_invoice_line_ids()
            
        for line in self.with_context(lang="es_CL").invoice_line_ids:
            if not line.account_id:
                continue
            product = line.product_id.default_code != "NO_PRODUCT"
            lines = {}
            lines["NroLinDet"] = line.sequence
            if product and (line.product_id.default_code or line.product_id.barcode):
                lines["CdgItem"] = []
                if line.product_id.default_code:
                    lines["CdgItem"].append({
                        "TpoCodigo": "INT1",
                        "VlrCodigo": line.product_id.default_code
                    })
                if line.product_id.barcode:
                    lines["CdgItem"].append({
                        "TpoCodigo": "EAN13",
                        "VlrCodigo": line.product_id.barcode
                    })
            details = line.get_tax_detail()
            lines["Impuesto"] = details['impuestos']
            taxInclude = details['taxInclude']
            if details.get('cod_imp_adic'):
                lines['CodImpAdic'] = details['cod_imp_adic']
                if taxInclude and not details['desglose']:
                    raise UserError("Con impuestos adicionales...")
            if details.get('IndExe'):
                lines['IndExe'] = details['IndExe']
                if details['IndExe'] == 1:
                    MntExe += details['MntExe']
                else:
                    MontoNF += details['MntExe']
            lines["NmbItem"] = line.product_id.with_context(
                display_default_code=False).name
            if line.product_id.name != line.name:
                lines["DscItem"] = line.name.replace(line.name, lines['NmbItem'])
            MontoItem = 0
            qty = 0
            if product:
                qty = round(line.quantity, 4)
                if qty == 0:
                    qty = 1
                elif qty < 0:
                    raise UserError("Cantidad no puede ser menor que 0")
                uom_name = line.uom_id.with_context(
                    exportacion=self.document_class_id.es_exportacion()
                ).name_get()
                if uom_name:
                    lines["UnmdItem"] = uom_name[0][1][:4]
                price_unit = details['price_unit']
                lines["PrcItem"] = round(price_unit, 6)
                if currency_id:
                    lines["OtrMnda"] = {}
                    lines["OtrMnda"]["PrcOtrMon"] = round(
                        currency_base._convert(
                            price_unit, currency_id, self.company_id, self.date_invoice, round=False
                        ),
                        4,
                    )
                    lines["OtrMnda"]["Moneda"] = self._acortar_str(currency_id.name, 3)
                    lines["OtrMnda"]["FctConv"] = round(currency_id.rate, 4)
                MontoItem = line.price_subtotal
                if taxInclude:
                    MontoItem = line.price_total
                if line.discount > 0:
                    lines["DescuentoPct"] = line.discount
                    DescMonto = line.discount_amount
                    if details['desglose']:
                        DescMonto = line.invoice_line_ids.compute_all(
                            DescMonto, self.currency_id, 1,
                            line.product_id, self.partner_id, discount=0,
                            uom_id=line.uom_id)['total_excluded']
                    lines["DescuentoMonto"] = DescMonto
                    if currency_id:
                        lines["OtrMnda"]["DctoOtrMnda"] = currency_base._convert(
                            DescMonto, currency_id, self.company_id, self.date_invoice
                        )
                if line.discount < 0:
                    lines["RecargoPct"] = line.discount * -1
                    RecargoMonto = line.discount_amount * -1
                    if details['desglose']:
                        RecargoMonto = line.invoice_line_ids.compute_all(
                            RecargoMonto, self.currency_id, 1,
                            line.product_id, self.partner_id, discount=0,
                            uom_id=line.uom_id)['total_excluded']
                    lines["RecargoMonto"] = RecargoMonto
                    if currency_id:
                        lines["OtrMnda"]["RecargoOtrMnda"] = currency_base._convert(
                            RecargoMonto, currency_id, self.company_id, self.date_invoice
                        )
                if currency_id:
                    lines["OtrMnda"]["MontoItemOtrMnda"] = currency_base._convert(
                        MontoItem, currency_id, self.company_id, self.date_invoice
                    )
                if taxInclude and details['desglose']:
                    taxInclude = False
            lines["QtyItem"] = qty
            lines["MontoItem"] = MontoItem
            
            # ==============================================
            # LÍNEAS ORIGINALES COMENTADAS/ELIMINADAS:
            # if lines["MontoItem"] < 0:
            #    raise UserError(_("No pueden ir valores negativos en las líneas de detalle"))
            # ==============================================
            
            if lines.get("PrcItem", 1) == 0:
                del lines["PrcItem"]
            invoice_lines.append(lines)
        return {
            "Detalle": invoice_lines,
            "MntExe": MntExe,
            "product": product,
            "tax_include": taxInclude,
            "MontoNF": MontoNF,
        }