from odoo import fields, models


class ObserveDocumentWizard(models.TransientModel):
    _name = 'observe.document.wizard'
    _description = 'Asistente para la observación de un documento'

    request_line_id = fields.Many2one(comodel_name='request.line')
    comment = fields.Text(string='Comentario', required=True)

    def prueba(self):
        request_id = self.request_line_id.request_id
        body = '''
            <p>Observación en adjunto: <strong>{}</strong></p>
            <p>Detalle:</p>
            <p class="text-danger"><strong>{}</strong></p>
        '''.format(self.request_line_id.document, self.comment)
        self.env['mail.message'].create({
            'message_type': 'comment',
            'model': 'request',
            'res_id': request_id.id,
            'subject': f'{request_id.op_admission_id.application_number} - {request_id.partner_id.name}',
            'subtype_id': self.env.ref('mail.mt_comment').id,
            'author_id': request_id.partner_id.id,
            'body': body
        })
        self.request_line_id.write({
            'state': 'observed',
            'comment': self.comment
        })
        