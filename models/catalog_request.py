from odoo import fields, models


class CatalogRequest(models.Model):
    _name = 'catalog.request'

    name = fields.Char(string='Nombre')
    description = fields.Html(string='Descripción')
    catalog_request_line_ids = fields.One2many(comodel_name='catalog.request.line', inverse_name='catalog_request_id')


class CatalogRequestLine(models.Model):
    _name = 'catalog.request.line'

    document = fields.Char(string='Documento')
    catalog_request_id = fields.Many2one(comodel_name='catalog.request')
