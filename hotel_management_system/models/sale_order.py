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

#Odoo Module
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

#=== GLOBAL DOMAIN ===#

STATUS_DOMAIN = ('status_bar', 'not in', ['cancel', 'checkout'])

class SaleOrder(models.Model):
    """Sale order

    Parameters
    ----------
    models : model

    """
    _inherit = "sale.order"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    hotel_check_in = fields.Datetime('Check In', required=False,
                                     help="Date of the arrival.")
    booking_id = fields.Many2one(
        "hotel.booking", "Booking")
    hotel_check_out = fields.Datetime('Check Out', required=False,
                                      help="Date of the departure.")
    booking_count = fields.Integer('Booking count', copy = False)
    is_room_type = fields.Boolean("Is Room Type")
    booking_line_id = fields.Many2one("hotel.booking.line", "Room No")

    # -------------------------------------------------------------------------
    # VALIDATION METHOD
    # -------------------------------------------------------------------------

    @api.constrains('hotel_check_in', 'hotel_check_out')
    def _check_validity_check_in_check_out(self):
        """ verifies if check_in is earlier than check_out. """
        for booking in self:
            if booking.hotel_check_in and booking.hotel_check_in < fields.Datetime.today():
                raise ValidationError(
                    _('"Check In" time cannot be earlier than Today time.'))
            if booking.hotel_check_in and booking.hotel_check_out:
                if booking.hotel_check_out < booking.hotel_check_in:
                    raise ValidationError(
                        _('"Check Out" time cannot be earlier than "Check In" time.'))

    def _confirm_room_for_booking(self, room_type_booking_line):
        """Here we are validating booking room that order rooms are booked parallel or not

        Parameters
        ----------
        room_type_booking_line : object
            booking line that has room type producta

        Returns
        -------
        recordset
            if any booking find
        """
        booking_rooms = room_type_booking_line.mapped('product_id')
        booking_ids = self.env['hotel.booking'].search([STATUS_DOMAIN,('booking_line_ids.product_id', 'in', booking_rooms.ids)])
        return booking_ids.filter_booking_based_on_date(self.hotel_check_in, self.hotel_check_out)

    def _pricelist_validation_for_booking_service(self):
        if self.booking_line_id:
            return True if self.pricelist_id == self.booking_line_id.booking_id.pricelist_id else False

    # -------------------------------------------------------------------------
    # OVERRIDE ACTION CONFIRM METHOD
    # -------------------------------------------------------------------------

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        if self.booking_count > 0:
            res.update({'booking_count': self.booking_count})
        return res

    def action_confirm(self):
        """

        Returns
        True
        """
        flag = self._pricelist_validation_for_booking_service()
        if flag is False:
            raise ValidationError(_("A different price list has been detected, please remember that pricelist will be same as booking pricelist..."))
        res = super(SaleOrder, self).action_confirm()
        room_type_booking_line = self.order_line.filtered(
            'product_id.product_tmpl_id.is_room_type')
        if room_type_booking_line:
            booking_ids = self._confirm_room_for_booking(room_type_booking_line)
            if not booking_ids:
                self.env['hotel.booking'].create({
                    'partner_id': self.partner_id.id,
                    'order_id': self.id,
                    'check_in': self.hotel_check_in,
                    'check_out': self.hotel_check_out,
                    'booking_line_ids': [(0, 0, {"product_id": line.product_id.id, 'price': line.price_unit, 'tax_ids': line.tax_id, 'subtotal_price': line.price_subtotal, 'guest_info_ids':line.guest_info_ids, }) for line in self.order_line if line.product_id.product_tmpl_id.is_room_type],
                    'pricelist_id': self.pricelist_id.id,
                    'booking_reference': 'sale_order',
                    'amount_untaxed': self.amount_untaxed,
                    'tax_amount': self.amount_tax,
                    'total_amount': self.amount_total,
                    'status_bar': 'confirm',
                })
                self.booking_count += 1
            else:
                self.message_post(body=_("<span class='text-danger'>Some rooms are not available...</span>"))
        return res

    def action_cancel(self):

        """

        Returns
        -------
        Boolean
        """

        res = super(SaleOrder, self).action_cancel()
        booking_id = self.env['hotel.booking'].search(
            [('order_id', '=', self.id)])
        if booking_id.status_bar != "allot":
            booking_id.status_bar = "cancel"
        return res


     # -------------------------------------------------------------------------
    # ACTION TO OPEN VIEW
    # -------------------------------------------------------------------------

    def action_view_booking(self):
        """Open Booking view

        Returns
        -------
        Open view
        """
        booking_id = 0
        result = self.env['ir.actions.act_window']._for_xml_id(
            'hotel_management_system.action_hotel_booking_menu')
        # choose the view_mode accordingly
        if (self.booking_count == 1 or self.booking_line_id):
            res = self.env.ref(
                'hotel_management_system.hotel_booking_view_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + \
                    [(state, view)
                     for state, view in result['views'] if view != 'form']
            else:
                result['views'] = form_view
            if self.booking_line_id:
                booking_id=self.booking_line_id
            else:
                booking_id = self.env['hotel.booking'].search(
                    [('order_id', '=', self.id)])
            result['res_id'] = booking_id.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result

    # -------------------------------------------------------------------------
    # ONCHNAGE METHODS
    # -------------------------------------------------------------------------

    @api.onchange('booking_line_id')
    def _onchange_booking_line(self):
        if self.booking_line_id:
            self.partner_id = self.booking_line_id.booking_id.partner_id.id
            self.hotel_check_in = self.booking_line_id.booking_id.check_in
            self.hotel_check_out = self.booking_line_id.booking_id.check_out


class SaleOrderLine(models.Model):
    """Sale order line inherit

    Parameters
    ----------
    models : model
    """
    _inherit = 'sale.order.line'

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    guest_info_ids = fields.One2many(
        'guest.info', 'sale_order_line_id', copy=False)
