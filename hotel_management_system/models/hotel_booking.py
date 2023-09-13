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
import datetime as dt
from datetime import datetime

# Odoo Module
from odoo import fields, models, api, _
from odoo.http import request
from odoo.exceptions import ValidationError


class HotelBooking(models.Model):
    """Module to manage Hotel Booking

    Parameters
    ----------
    models : importing Model
    """
    _name = "hotel.booking"
    _description = "Hotel Booking Management"
    _rec_name = "sequence_id"

    # -------------------------------------------------------------------------//
    # DEFAULT METHODS
    # -------------------------------------------------------------------------//
    def _default_pricelist_id(self):
        return self.env['product.pricelist'].search([
            '|', ('company_id', '=', False),
            ('company_id', '=', self.env.company.id)], limit=1)

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    sequence_id = fields.Char(string='Booking Reference', required=True,
                              copy=False, readonly=True, index=True, default=lambda self: _('New'))
    image_1920 = fields.Image(related='partner_id.image_1920')
    sale_order_ids = fields.One2many(
        'sale.order', 'booking_id', string="Sale Orders")
    user_id = fields.Many2one(
        'res.users', string='Salesperson',  default=lambda self: self.env.user)
    booking_generate = fields.Boolean('Booking Already Available')
    order_id = fields.Many2one('sale.order', 'Sale Order')
    booking_line_ids = fields.One2many(
        "hotel.booking.line", 'booking_id', string='Booking Line')
    partner_id = fields.Many2one('res.partner', 'Guest Name')
    check_in = fields.Datetime('Check In', required=True, default=fields.Datetime.now, tracking=True,
                               help="Start date of the arrival.")
    check_out = fields.Datetime('Check Out', tracking=True,
                                help="End date of the departure.")
    status_bar = fields.Selection(
        [('initial', 'Draft'), ('confirm', 'Confirm'), ('allot', 'Room Allocated'), ('cancel', 'Cancel'), ('checkout', 'Checkout')], default='initial', copy=False)
    booking_reference = fields.Selection(
        [('sale_order', 'Sale order'), ('manual', 'Manual'), ], default='manual', copy=False, string="Reference")
    pricelist_id = fields.Many2one(
        'product.pricelist', string='Pricelist',
        required=True, readonly=False, default = _default_pricelist_id)
    currency_id = fields.Many2one(related='pricelist_id.currency_id', depends=[
                                  "pricelist_id"], store=True, string='Currency')
    amount_untaxed = fields.Monetary(
        'Amount Untaxed', compute="_compute_actual_amount")
    total_amount = fields.Monetary(
        'Total amount')
    booking_discount = fields.Monetary('Discount')
    tax_amount = fields.Monetary(
        string='Tax Amount')
    docs_ids = fields.Many2many('ir.attachment', string="Document")
    doc_description = fields.Text("Document Description")

    # -------------------------------------------------------------------------//
    # FILTER BOOKING
    # -------------------------------------------------------------------------//

    def filter_booking_based_on_date(self, check_in, check_out):
        """_summary_

        Parameters
        ----------
        check_in : date type field
        check_out : date type field

        Returns
        -------
        Filtered booking object that are already booked
        """
        check_in = check_in.date()
        check_out = check_out.date()
        return self.filtered(lambda r: r if r.status_bar not in ('cancel', 'checkout') and ((r.check_in).date() == check_in or
                                                                                            ((r.check_in).date() <= check_in and
                                                                                             (r.check_out).date() > check_in) or
                                                                                            ((r.check_in).date() <= check_in and
                                                                                             (r.check_out).date() > check_in) or
                                                                                            (((r.check_in).date() >= check_in and
                                                                                              (r.check_in).date() <= check_out) or
                                                                                             (((r.check_in).date() <= check_in and
                                                                                               (r.check_out).date() <= check_out) and
                                                                                                (r.check_out).date() > check_in) or
                                                                                             ((r.check_in).date() <= check_out and
                                                                                                (r.check_out).date() > check_in)))
                             else None)

    # -------------------------------------------------------------------------
    # CONSTRAINT METHODS
    # -------------------------------------------------------------------------

    @api.constrains('check_in', 'check_out')
    def _check_validity_check_in_check_out_booking(self):
        """ verifies if check_in is earlier than check_out. """
        for booking in self:
            if booking.check_in and booking.check_in < fields.Datetime.today():
                raise ValidationError(
                    _('"Check In" time cannot be earlier than Today time.'))
            if booking.check_in and booking.check_out:
                if booking.check_out < booking.check_in:
                    raise ValidationError(
                        _('"Check Out" time cannot be earlier than "Check In" time.'))

    # **********************************************************
    # In future we would combine this function with fetch_booking_count_for_dashboard
    # **********************************************************

    def fetch_data_for_dashboard(self, **kwarg):
        """ fetch data for dashborad reload """

        fetch_data = {}
        product = self.env['product.product']
        booking = self.env['hotel.booking']
        room_type_product = product.search(
            [('is_room_type', '=', True), ('active', '=', True)])

        # we are calculating booked rooms that are not available today date
        today_date = datetime.combine(fields.Date.today(), datetime.min.time())
        today_booking = booking.search([('check_out', '>', today_date.date()), ('check_in', '<=', datetime.combine(
            today_date, dt.time.max)), ('status_bar', 'not in', ['initial', 'checkout'])])
        booked_room = today_booking.mapped('booking_line_ids.product_id')

        available_rooms = (room_type_product - booked_room)
        fetch_data.update({'booked_room': len(booked_room),
                          'available_rooms': len(available_rooms),
                           'booked_room_ids': booked_room.ids})
        room_data = self.env['product.template'].search(
            [['is_room_type', '=', True]]).read(['name', 'product_variant_count'])
        current_date_check_in = self.search(
            [('check_in', '>=', today_date), ('check_in', '<', today_date + dt.timedelta(days=1)), ('status_bar', 'not in', ['checkout', 'cancel'])])
        current_date_check_out = self.search(
            [('check_out', '>=', today_date), ('check_out', '<', today_date + dt.timedelta(days=1)), ('status_bar', '=', 'allot')])
        fetch_data.update({'room_data': room_data, 'check_in_booking': current_date_check_in.ids, 'check_out_booking': current_date_check_out.ids,
                          'current_date_check_in': len(current_date_check_in), 'current_date_check_out': len(current_date_check_out)})
        return fetch_data

    def get_booked_and_available_rooms(self, selected_date):
        """ method will use to calculate booked and available rooms """

        product = self.env['product.product']
        booking = self.env['hotel.booking']
        # total room that are available for booking
        room_type_product = product.search(
            [('is_room_type', '=', True), ('active', '=', True)])
        not_available_booking = booking.search(
            [('check_out', '>', selected_date.date()), ('check_in', '<=', datetime.combine(selected_date, dt.time.max)), ('status_bar', 'not in', ['initial', 'checkout'])])
        booked_rooms = not_available_booking.booking_line_ids.mapped(
            'product_id')  # getting rooms from booking
        # getting calculated available rooms
        available_rooms = (room_type_product - booked_rooms)
        return booked_rooms, available_rooms

    def get_count_of_booking(self, selected_date_data, today_date):
        """ fetch the booking id & count """

        product = self.env['product.product']
        booking = self.env['hotel.booking']
        date_eligible = True

        # case 1: In if condition we are checking that seelcted date is past date
        # case 2: if selected date is not past date then get check in/out booking
        selected_date = datetime.combine(
            selected_date_data, datetime.min.time())
        if selected_date_data < today_date:
            date_eligible, current_date_check_in, current_date_check_out, booked_rooms, available_rooms = [
                False, booking, booking, product, product]
        else:
            current_date_check_in = self.search(
                [('check_in', '>=', selected_date), ('check_in', '<', selected_date + dt.timedelta(days=1)), ('status_bar', 'in', ['confirm', 'initial', 'allot'])])
            current_date_check_out = self.search(
                [('check_out', '>=', selected_date), ('check_out', '<', selected_date + dt.timedelta(days=1)), ('status_bar', '=', 'allot')])

        # here we are getting booking that have checkout date after seletced date
        if date_eligible:
            booked_rooms, available_rooms = self.get_booked_and_available_rooms(
                selected_date)

        return {'current_month_check_in': len(current_date_check_in),
                'current_month_check_out': len(current_date_check_out),
                'check_in_booking': current_date_check_in.ids,
                'check_out_booking': current_date_check_out.ids,
                'booked_room_ids': booked_rooms.ids,
                'available_rooms': len(available_rooms),
                'available_rooms_name': available_rooms.read(["display_name", "product_tmpl_id"])
                }

    def fetch_booking_count_for_dashboard(self, **kwarg):
        """ fetching data onchange scale, possible values ['MONTH','YEAR','WEEK', 'DAY'] """

        selected_date = str(kwarg['calendar_data'].get('day'))+'/' + \
            str(kwarg['calendar_data'].get('month')) + \
            '/'+str(kwarg['calendar_data'].get('year'))
        today_date = fields.Date.today()
        return self.get_count_of_booking(datetime.strptime(selected_date, '%d/%m/%Y').date(), today_date)

    def current(self):
        """Checking groups

        Returns
        -------
        Object
        """
        if request and request.env.user.has_group('base.group_portal'):
            return self.filtered(lambda _: _.product_id.sudo().website_published)
        return self

    # -------------------------------------------------------------------------
    # ACTION TO OPEN VIEW
    # -------------------------------------------------------------------------

    def action_view_order(self):
        """Opening View

        Returns
        -------
        View
        """
        order_id = 0
        result = self.env['ir.actions.act_window']._for_xml_id(
            'sale.action_quotations_with_onboarding')
        # choose the view_mode accordingly
        res = self.env.ref(
            'sale.view_order_form', False)
        form_view = [(res and res.id or False, 'form')]
        if 'views' in result:
            result['views'] = form_view + \
                [(state, view)
                    for state, view in result['views'] if view != 'form']
        else:
            result['views'] = form_view
        order_id = self.env['sale.order'].search(
            [('id', '=', self.order_id.id)])
        result['res_id'] = order_id.id
        return result

    def sale_order_view(self):
        """Sale order View

        Returns
        -------
        Open View in tree mode
        """
        active_id = self.id
        domain = []
        context = {
                'default_booking_id': self.id,
                'default_partner_id': self.partner_id.id,
                'default_hotel_check_in': self.check_in,
                'default_hotel_check_out': self.check_out,
            }
        if self.sale_order_ids:
            view = 'tree,form'
            domain = [('booking_id', '=', active_id)]
        else:
            view = "form,tree"
        return {
            "name": "Sale Order",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": view,
            'domain': domain,
            "target": "current",
            "context": context,
        }

    # -------------------------------------------------------------------------
    # CONFIRM BOOKING ACTION
    # -------------------------------------------------------------------------

    def action_confirm_booking(self):
        """Action for confirm button

        Raises
        ------
        ValidationError
            Show error if room is not availabel in booking line
        """

        # //-------------------------- checking date validation -----------------------//
        self._check_validity_check_in_check_out_booking()

        if self.status_bar == "initial":
            if not self.booking_line_ids:
                raise ValidationError(
                    _("Please add rooms for booking confirmation..."))
            else:
                sale_order = self.env['sale.order'].create({
                    'partner_id': self.partner_id.id,
                    'hotel_check_in': self.check_in,
                    'hotel_check_out': self.check_out,
                    'state': 'sale',
                    'pricelist_id': self.pricelist_id.id,
                    'order_line': [(0, 0, {"product_id": line.product_id.id, 'tax_id': line.tax_ids, 'price_unit': line.subtotal_price, 'guest_info_ids': line.guest_info_ids}) for line in self.booking_line_ids],
                })
                self.order_id = sale_order
                self.status_bar = "confirm"
                self.booking_line_ids.mapped('product_id').write(
                    {'is_room_booked': True})

    #=== CRUD METHODS ===#

    @ api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])

            if vals.get('sequence_id', _('New')) == _('New'):
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(
                    vals['check_in'])) if 'check_in' in vals else None
                vals['sequence_id'] = self.env['ir.sequence'].next_by_code(
                    'hotel.booking', sequence_date=seq_date) or _('New')

        return super().create(vals_list)

    def _valid_field_parameter(self, field, name):
        # EXTENDS models
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    # -------------------------------------------------------------------------
    # DEPENDS METHODS
    # -------------------------------------------------------------------------

    @ api.depends('booking_line_ids.subtotal_price')
    def _compute_actual_amount(self):
        for booking in self:
            total_tax_amount = 0
            total_amount = 0
            for line in booking.booking_line_ids:
                total_tax_amount += line.taxed_price
                total_amount += line.subtotal_price
            booking.tax_amount = total_tax_amount - total_amount
            booking.amount_untaxed = total_amount
            booking.total_amount = total_tax_amount


    def action_checkout(self):
        self.status_bar="checkout"


class HotelBookingLine(models.Model):
    """Booking Line model

    Parameters
    ----------
    models : Model

    """
    _name = "hotel.booking.line"
    _description = "Booking Line"
    _rec_name = "booking_sequence_id"  # missing name field

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    booking_sequence_id = fields.Char(string='Booking Line Reference', required=True,
                                      copy=False, readonly=True, index=True, default=lambda self: _('New'))
    image_1920 = fields.Image(related='product_id.image_1920')
    product_id = fields.Many2one('product.product', string='Rooms')
    booking_id = fields.Many2one('hotel.booking',  readonly=True, copy=False)
    guest_info_ids = fields.One2many('guest.info', 'booking_id')
    price = fields.Float(string='Price Per Night', store=True)
    description = fields.Text('Description', compute="_get_description" , store=True)
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    booking_days = fields.Integer(
        string='Days Book For', compute="_compute_booking_days")
    subtotal_price = fields.Float(string='Subtotal', compute="_compute_amount")
    taxed_price = fields.Float(
        string='taxed amount', compute="_compute_amount")
    currency_id = fields.Many2one(
        related='booking_id.currency_id', string='Currency')
    status_bar = fields.Selection(
        [('initial', 'Draft'), ('confirm', 'Confirm'), ('allot', 'Room Allocated'), ('cancel', 'Cancel'), ('checkout', 'Checkout')], default='initial', copy=False, compute="_compute_status")

    # -------------------------------------------------------------------------
    # DEPENDS & ONCHANGE METHODS
    # -------------------------------------------------------------------------

    @ api.depends('booking_id.status_bar')
    def _compute_status(self):
        for line in self:
            line.status_bar = line.booking_id.status_bar

    @ api.depends('booking_id.check_out', 'booking_id.check_in')
    def _compute_booking_days(self):
        for day in self:
            if day.booking_id.check_in and day.booking_id.check_out:
                day.booking_days = (
                    day.booking_id.check_out - day.booking_id.check_in).days
            else:
                day.booking_days = False

    @ api.onchange('subtotal_price')
    @ api.depends('product_id', 'price', 'tax_ids', 'subtotal_price', 'booking_id.check_out', 'booking_id.check_in')
    def _compute_amount(self):
        for line in self:
            price = line.price
            taxes = line.tax_ids.compute_all(price, line.booking_id.currency_id, 1,
                                            product=line.product_id)
            line.subtotal_price = taxes['total_excluded']*line.booking_days
            line.taxed_price = taxes['total_included']*line.booking_days

    @api.depends('product_id', 'booking_id.pricelist_id', 'booking_days')
    def _get_description(self):
        for line in self:
            if line.product_id.description_sale: 
                line.description = line.product_id.description_sale
            else:
                line.description = ' '
            if line.booking_id.pricelist_id:
                line.price = line.booking_id.pricelist_id._get_product_price(line.product_id, line.booking_days)

    # -------------------------------------------------------------------------
    # OPEN VIEW FOR ROOM SERVICES
    # -------------------------------------------------------------------------

    def sale_order_view(self):
        """Sale order View

        Returns
        -------
        Open View in tree mode
        """
        active_id = self.id
        return {
            "name": "Sale Order",
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "view_mode": 'tree',
            'domain': [('booking_line_id', '=', active_id)],
            "target": "new",
        }

    #=== CRUD METHODS ===#

    @ api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if 'company_id' in vals:
                self = self.with_company(vals['company_id'])
            if vals.get('booking_sequence_id', _('New')) == _('New'):
                vals['booking_sequence_id'] = self.env['ir.sequence'].next_by_code(
                    'hotel.booking.line') or _('New')

        return super().create(vals_list)
    