from odoo import fields, models

STATE_SELECTION = [
    ('received', 'Recibido'),
    ('in_progress', 'En proceso'),
    ('finalized', 'Finalizado'),
]


class Request(models.Model):
    _name = 'request'
    _rec_name = 'op_admission_id'

    op_admission_id = fields.Many2one(comodel_name='op.admission', string='Admisión', required=True)
    partner_id = fields.Many2one(related='op_admission_id.partner_id', store=True)
    batch_id = fields.Many2one(related='op_admission_id.batch_id')
    course_id = fields.Many2one(related='op_admission_id.course_id')
    application_number = fields.Char(related='op_admission_id.application_number')
    catalog_request_id = fields.Many2one(comodel_name='catalog.request', string='Catálogo de solicitudes', required=True)
    description = fields.Html(string='Descripción')
    request_line_ids = fields.One2many(comodel_name='request.line', inverse_name='request_id', string='Adjuntos')
    state = fields.Selection(selection=STATE_SELECTION, default='received', string='Estado')

    def action_in_progress(self):
        list_request_line_ids = [(5, 0, 0)]
        list_request_line_ids.extend(
            [(0, 0, {'document': line.document}) for line in self.catalog_request_id.catalog_request_line_ids])
        self.write({
            'request_line_ids': list_request_line_ids,
            'state': 'in_progress'
        })
        