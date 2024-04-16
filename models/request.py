from odoo import api, fields, models

STATE_SELECTION = [
    ('on_hold', 'En espera'),
    ('accepted', 'Aceptado'),
    ('observed', 'Observado'),
]


class Request(models.Model):
    _name = 'request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'op_admission_id'

    op_admission_id = fields.Many2one(comodel_name='op.admission', string='Admisión', required=True)
    partner_id = fields.Many2one(related='op_admission_id.partner_id', store=True)
    batch_id = fields.Many2one(related='op_admission_id.batch_id')
    course_id = fields.Many2one(related='op_admission_id.course_id')
    application_number = fields.Char(related='op_admission_id.application_number')
    catalog_request_id = fields.Many2one(comodel_name='catalog.request', string='Catálogo de solicitudes',
                                         required=True)
    description = fields.Html(string='Descripción')
    request_line_ids = fields.One2many(comodel_name='request.line', inverse_name='request_id', string='Adjuntos')
    state = fields.Selection(selection=STATE_SELECTION, default='on_hold', string='Estado', compute='_compute_state',
                             store=True, tracking=True)
    hide_status = fields.Boolean(default=False)
    # comment = fields.Text(string='Comentario', compute='_compute_comment', tracking=True, store=True)

    # @api.depends('request_line_ids.comment')
    # def _compute_comment(self):
    #     for request in self:
    #         comment = ''
    #         if request.request_line_ids:
    #             for request_line in request.request_line_ids:
    #                 comment = request_line.comment
    #         request.write({'comment': comment})

    @api.depends('request_line_ids.state')
    def _compute_state(self):
        for request in self:
            request_line_status = request.request_line_ids.mapped(lambda x: x.state)
            if all(state == 'on_hold' for state in request_line_status):
                request.write({'state': 'on_hold'})
            elif all(state == 'accepted' for state in request_line_status):
                request.write({'state': 'accepted'})
            elif any(state == 'observed' for state in request_line_status):
                request.write({'state': 'observed'})
            else:
                request.write({'state': 'on_hold'})

    def action_confirm(self):
        list_request_line_ids = [(5, 0, 0)]
        list_request_line_ids.extend(
            [(0, 0, {'document': line.document}) for line in self.catalog_request_id.catalog_request_line_ids])
        self.write({
            'request_line_ids': list_request_line_ids,
            'hide_status': True
        })
        