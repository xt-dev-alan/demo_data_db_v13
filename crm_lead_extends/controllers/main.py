# -*- coding: utf-8 -*-

import logging
import json
from datetime import date as dt

from odoo import http
from odoo.http import request as Request

_logger = logging.getLogger(__name__)

ACTIVITY_TYPE = {   'Llamada': 'mail.mail_activity_data_call',
                    'Email': 'mail.mail_activity_data_email',
                    'Whatsapp': 'crm_lead_extends.mail_activity_whatsapp'
                }


class LeadController(http.Controller):

    @http.route('/lead/outside', auth='public', methods=['POST'], csrf=False)
    def index(self, **kw):
        crm_lead = Request.env['crm.lead'].sudo()
        mail_activity = Request.env['mail.activity'].sudo()
        partner_id = Request.env['res.partner'].sudo().search([ ('email', '=', kw.get('email')) ], limit=1)
        values = ( kw.get('contact_way'), kw.get('name'), kw.get('phone'), kw.get('email'),  dt.today().strftime('%d-%m-%Y') )
        msg = "Forma de Contacto: %s\nNombre: %s\nPhone: %s\nEmail: %s\nFecha: %s\n\n"%values
        if partner_id:
            lead_id = crm_lead.search([('partner_id', '=', partner_id  )], limit=1)
        else:    
            lead_id = crm_lead.search([('email_from', '=', kw.get('email')  )], limit=1)
        if not lead_id:
            lead_id = crm_lead.create( {  
                                'name': "%s's Lead from MIRA.GT"%kw.get('name'),
                                'email_from': kw.get('email'),
                                'phone': kw.get('phone'),
                                'contact_name': kw.get('name')
                            } )
        
        mail_activity.create( {
                                'res_model_id': Request.env.ref('crm.model_crm_lead').id,
                                'res_id': lead_id.id,
                                'user_id' : lead_id.user_id.id,
                                'note': msg,
                                'date_deadline': dt.today(),
                                'activity_type_id': Request.env.ref( ACTIVITY_TYPE[ kw.get('contact_way') ] ).id, 
                                'summary': 'Lead from MIRA.GT'

                            } )                
        return Request.make_response( json.dumps( {'ok': True} ) )