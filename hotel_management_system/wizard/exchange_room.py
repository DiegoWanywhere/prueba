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
import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError
_log = logging.getLogger(__name__)


class ExchangeRoom(models.TransientModel):
    _name = "exchange.room"
    _description = "Exchange rooms if available"
    booking_line_id = fields.Many2one(
        'hotel.booking.line', string='Reference No')
    available_room_ids = fields.Many2many('product.product')
    exchange_room=fields.Many2one(
        'product.product', string='Exchange Room')

    @api.onchange('booking_line_id')
    def booking_line_compute(self):
        booking_line = self.env['hotel.booking.line'].browse(
            self._context.get("active_ids"))
        self.booking_line_id = booking_line
        self.available_room_ids = self._check_available_exchange_room(booking_line)

    # @api.onchange('booking_line_id')
    def _check_available_exchange_room(self,booking_line):

        if self.booking_line_id:
            self.available_room_ids = False
            active_booking = booking_line.booking_id

            check_in = active_booking.check_in
            check_out = active_booking.check_out
            # room_temp_id = self.booking_line_id.product_id.product_tmpl_id

            booking = self.env['hotel.booking'].search([])
            # booking=[]

            product_ids = self.env['product.product'].search([("product_tmpl_id.is_published", "=", True), ("product_tmpl_id.is_room_type", "=", True)])
            if booking:
                booked_booking_ids = booking.filter_booking_based_on_date(check_in, check_out)
                return product_ids - booked_booking_ids.mapped('booking_line_ids.product_id')

            # Now we want to show all type of available rooms at the time of exchange

            # eligible_products = self.env['product.product'].search(
            #     [("product_tmpl_id", "=", room_temp_id.id), ("product_tmpl_id.is_room_type", "=", True)])
            # if product_ids:
            #     final_available_products = eligible_products.filtered(
            #         lambda r: r if r.id not in product_ids else None)
            # else:
            #     final_available_products = eligible_products
            return product_ids

    def action_exchange_room(self):
        booking_line = self.env['hotel.booking.line'].browse(
            self._context.get("active_ids"))
        if self.exchange_room:
            booking_line.product_id = self.exchange_room.id
            return True
        else:
            return self.env['wk.wizard.message'].genrated_message("Exchange is not possible", name='Message')


class AvailableProduct(models.TransientModel):
    _name = "available.product"
    _description = "Available Rooms"
    name = fields.Char("Room Name")
    room_id = fields.Integer("Room Id", store=True)
    exchange_id = fields.Many2one("exchange.room")
    template_attribute_value_ids = fields.Many2many('product.template.attribute.value', string="Attribute Values")
