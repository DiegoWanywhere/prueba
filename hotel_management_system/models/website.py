# -*- coding: utf-8 -*-
##########################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>;)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>;
##########################################################################
# Python Module
from datetime import date, datetime
import logging
# Odoo Module
from odoo import api, fields, models
from odoo.http import request
from odoo.addons.website.models import ir_http

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    # -------------------------------------------------------------------------//
    # MODEL FIELD FOR SNIPPET
    # -------------------------------------------------------------------------//
    website_homepage_product_ids = fields.Many2many('product.template',string='Homepage Product')

    def sale_product_domain(self):
        """Add domain based on booking filter for snippet

        Returns
        -------
        list
            return domain
        """
        is_frontend = ir_http.get_request_website() #Checking that frontend active or not
        subdomain = []
        if is_frontend:
            if request.params.get('check_in',False) and request.params.get('check_out',False):
                subdomain = [('is_room_type', '=', True)]
                check_in = datetime.strptime(
                    (request.session['check_in']), '%Y-%m-%d')
                check_out = datetime.strptime(
                    (request.session['check_out']), '%Y-%m-%d')
                booking = request.env['hotel.booking'].search([])
                all_room_type_products = request.env['product.product'].search(subdomain)
                # filtering booking for not eligible rooms
                filtered_booking = booking.filter_booking_based_on_date(check_in, check_out)
                product_ids = filtered_booking.mapped('booking_line_ids.product_id')
                available_rooms = (all_room_type_products - filtered_booking.mapped('booking_line_ids.product_id')).mapped('product_tmpl_id')
                domain = [('id', 'in', available_rooms.ids)]
                subdomain = ['&'] + subdomain + domain
        if subdomain:
            return ['&'] + super(Website, self).sale_product_domain() + subdomain
        else:
            return super(Website, self).sale_product_domain()

    # -------------------------------------------------------------------------//
    # Snippet demo data load
    # -------------------------------------------------------------------------//

    @api.model
    def hotel_management_system_snippet_data(self):
        default_website = self.env['website'].search([],limit=1)
        room_type_product = self.env['product.template'].search([('is_room_type', '=', True),('active','=', True)],limit=12)
        default_website.website_homepage_product_ids = room_type_product

    @api.model
    def get_wire_transfer(self):
        try:
            wire_transfer = self.env.ref('payment.payment_provider_transfer', raise_if_not_found=False)
            if wire_transfer.module_id.state != 'installed' :
                wire_transfer.module_id.button_install()
                return wire_transfer.write({
                    'name': 'Pay at Hotel',
                    'state': 'test',
                    'website_id': False,
                    'is_published': True,
                }) if wire_transfer else False
            return wire_transfer.write({
                'name': 'Pay at Hotel',
                'is_published': True,
            }) if wire_transfer else False
        except Exception as e:
            _logger.info("Couldn't install Wire Transfer due to an error.")
            _logger.info(e)
            return False


