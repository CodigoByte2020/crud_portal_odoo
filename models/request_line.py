from odoo import fields, models


class RequestLine(models.Model):
    _name = 'request.line'

    request_id = fields.Many2one(comodel_name='request', string='Solicitud')
    document = fields.Char(string='Documento', readonly=True)
    filename = fields.Char(string='Nombre de archivo')
    file = fields.Binary(attachment=True, string='Archivo')
