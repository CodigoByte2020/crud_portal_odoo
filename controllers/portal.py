from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal, pager
from odoo.http import request


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(CustomerPortal, self)._prepare_home_portal_values(counters)
        user_id = request.env.uid
        current_user = request.env['res.users'].sudo().browse(user_id)
        domain = [
            ('partner_id', '=', current_user.partner_id.id),
            ('op_admission_id.state', '=', 'done')
        ]
        values['requests_quantity'] = request.env['request'].sudo().search_count(domain)  # FIXME: CUANDO HAY 0 NO SE MUESTRA :(
        return values

    @http.route(['/my/requests', '/my/requests/page/<int:page>'], type='http', website=True)
    def request_list_view(self, page=1, **kwargs):
        step = 5
        request_model = request.env['request'].sudo()
        user_id = request.env.uid
        current_user = request.env['res.users'].sudo().browse(user_id)
        domain = [
            ('partner_id', '=', current_user.partner_id.id),
            ('op_admission_id.state', '=', 'done')
        ]
        my_requests_quantity = request_model.search_count(domain)
        page_detail = pager(
            url='/my/requests',
            total=my_requests_quantity,
            page=page,
            step=step
        )
        my_requests = request_model.search(domain, limit=step, offset=page_detail['offset'])
        success_message = request.params.get('success_message', False)
        values = {
            'my_requests': my_requests,
            'page_name': 'request_list_view',
            'pager': page_detail,
            'success_message': success_message
        }
        return request.render('isep_requests.request_list_view', values)

    @http.route('/my/requests/<int:request_id>', type='http', website=True)
    def request_form_view(self, request_id, **kwargs):
        user_id = request.env.uid
        current_user = request.env['res.users'].sudo().browse(user_id)
        domain = [
            ('partner_id', '=', current_user.partner_id.id),
            ('op_admission_id.state', '=', 'done')
        ]
        request_model = request.env['request'].sudo()
        current_request = request_model.browse(request_id)
        request_ids = request_model.search(domain).ids
        request_index = request_ids.index(request_id)
        values = {
            'current_request': current_request,
            'page_name': 'request_form_view',
            'prev_record': request_index != 0 and f'/my/requests/{request_ids[request_index - 1]}',
            'next_record': request_index < len(request_ids) - 1 and f'/my/requests/{request_ids[request_index + 1]}'
        }
        return request.render('isep_requests.request_form_view', values)

    @http.route('/my/requests/catalogs', type='http', methods=['GET'], auth='public', website=True)
    def catalog_form_view(self, **kwargs):
        catalog_requests = request.env['catalog.request'].sudo().search([])
        admissions = request.env['op.admission'].sudo().search([])
        values = {
            'page_name': 'catalog_form_view',
            'catalog_requests': catalog_requests,
            'admissions': admissions
        }
        return request.render('isep_requests.catalog_form_view', values)

    @http.route('/my/requests/new_request', type='http', methods=['GET', 'POST'], auth='public', website=True)
    def new_request_form_view(self, **kwargs):
        catalog_request_model = request.env['catalog.request'].sudo()
        op_admission_model = request.env['op.admission'].sudo()
        values = {
            'page_name': 'new_request_form_view',
            'catalog_request_line_ids': []
        }

        if request.httprequest.method == 'GET':
            catalog_request_id = kwargs.get('catalogs', False)
            admission_id = kwargs.get('admissions', False)
            if catalog_request_id:
                catalog = catalog_request_model.browse(int(catalog_request_id))
                catalog_request_line_ids = catalog.catalog_request_line_ids
                values.update({
                    'catalog': catalog,
                    'catalog_request_line_ids': catalog_request_line_ids
                })
            if admission_id:
                admission = op_admission_model.browse(int(admission_id))
                values.update({
                    'admission': admission,
                    'partner_id': admission.partner_id,
                    'batch_id': admission.batch_id,
                    'course_id': admission.course_id,
                    'application_number': admission.application_number
                })

        elif request.httprequest.method == 'POST':
            success_message = 'Solicitud registrada con éxito'
            values_request = {}
            if kwargs.get('catalogs', False):
                catalog_request_id = catalog_request_model.browse(int(kwargs['catalogs']))
                values_request['catalog_request_id'] = catalog_request_id.id
            if kwargs.get('admissions', False):
                op_admission_id = op_admission_model.browse(int(kwargs['admissions']))
                values_request.update({
                    'op_admission_id': op_admission_id.id,
                    'partner_id': op_admission_id.partner_id.id
                })
            request.env['request'].sudo().create(values_request)  # TODO: FALTA VER QUE SE CREEN LOS ATTACHMENTS
            return request.redirect(f'/my/requests?success_message={success_message}')

        return request.render('isep_requests.new_request_form_view', values)
