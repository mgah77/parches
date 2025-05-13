from odoo import models

class UploadXMLWizardCustom(models.Model):
    _inherit = 'sii.dte.upload_xml.wizard'

    def _read_xml(self, mode="text", check=False):
        xml = (
            self._get_xml()
            .replace('<?xml version="1.0" encoding="ISO-8859-1"?>', "")
            .replace('<?xml version="1.0" encoding="ISO-8859-1" ?>', "")
            .replace('<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>', "")
	    .replace('<VlrCodigo>GASTOS_DESP</VlrCodigo>', "")
	    .replace('ds:', "")
	    .replace('<ImptoReten>', "")
	    .replace('</ImptoReten>', "")
        .replace('<CodImpAdic>28</CodImpAdic>', "")
        )
        if check:
            return xml
        xml = xml.replace(' xmlns="http://www.sii.cl/SiiDte"', "")
        if mode == "etree":
            parser = etree.XMLParser(remove_blank_text=True)
            return etree.fromstring(xml, parser=parser)
        return xml