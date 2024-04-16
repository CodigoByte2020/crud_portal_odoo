from odoo import fields, models


class ObserveDocumentWizard(models.TransientModel):
    _name = 'observe.document.wizard'
    _description = 'Asistente para la observación de un documento'

    request_line_id = fields.Many2one(comodel_name='request.line')
    comment = fields.Text(string='Comentario', required=True)  # TODO: FALTA GUARDAR EL COMENTARIO EN LA BD ???

    def prueba(self):
        print('prueba')
        self.request_line_id.write({
            'state': 'observed',
            'comment': self.comment
        })
