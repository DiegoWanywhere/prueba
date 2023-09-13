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
from datetime import datetime

# Odoo Module
from odoo import fields, models, api
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    """_summary_

    Parameters
    ----------
    models : model

    Raises
    ------
    UserError
        If validation failed
    """
    _inherit = "product.template"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    is_room_type = fields.Boolean("Is Room Type")
    max_adult = fields.Integer("Max Adult", default=1)
    max_child = fields.Integer("Max Children")
    service_ids = fields.Many2many("hotel.service", string="Services")
    facility_ids = fields.Many2many("hotel.facility", string="Facility")
    product_website_description = fields.Text('Product Description')
    room_policy = fields.Html('Room Policy')

    # -------------------------------------------------------------------------
    # USING IN DEMO DATA
    # -------------------------------------------------------------------------
    @api.model
    def get_room_multiline_policy_description(self):
        description = """
                    <ol><li><p>Check-in and check-out times: hotels have set check-in and check-out times
                    that guests must follow. typically check-in
                    time is in the afternoon, and check-out time is in the morning.</p></li><li><p>Occupancy
                    limits: Hotel rooms have a maximum occupancy limit, which means that only a certain
                    number of people are allowed to stay in the room. This is often determined by the number
                    of beds in the room.</p></li><li><p>Smoking policy: Hotels have a strict no-smoking policy,
                    which means that smoking is not allowed in the rooms or anywhere else on the property. If you
                    are caught smoking, you may be charged a fee or asked to leave.</p></li><li><p>Pet policy:
                    Hotels allow pets, while others do not. If a hotel allows pets, there may be a fee or restrictions
                    on the size or breed of pet allowed.</p></li><li><p>Damage policy: Guests are responsible for any
                    damage caused to the hotel room during their stay. If any damage is found after the guest checks out,
                    the hotel may charge the guest for the repairs.</p></li><li><p>Noise policy: Guests are expected to
                    keep noise levels to a minimum to avoid disturbing other guests. Hotels have quiet hours during
                    which noise must be kept to a minimum.</p></li><li><p>Payment policy: Most hotels require a credit card
                    or other form of payment at the time of booking or check-in. Hotels may require a deposit or hold on
                    the credit card in case of any incidental charges.</p></li></ol>
                """
        room_type_product_ids = self.search([('is_room_type', '=', True)])
        room_type_product_ids.write({'room_policy': description})

    # -------------------------------------------------------------------------
    # FETCH DATA FOR DASHBOARD ROOMS
    # -------------------------------------------------------------------------

    def fetch_data_for_room(self, **kwargs):
        """fetching room information for dashboard

        Returns
        -------
        dict
            Room data
        """

        room_record = self.read(
            ["name", "max_adult", "max_child"])
        selected_date = str(kwargs['selected_date'].get('day'))+'/' + \
            str(kwargs['selected_date'].get('month')) + \
            '/'+str(kwargs['selected_date'].get('year'))
        datetime_date = datetime.strptime(selected_date, '%d/%m/%Y')
        if datetime_date.date() < fields.Date.today():
            available_rooms = self.env['product.product']
        else:
            _, available_rooms = self.env['hotel.booking'].get_booked_and_available_rooms(
                datetime_date)
        room_variant_data = available_rooms.filtered(
            lambda r: r if r.product_tmpl_id == self else None)
        room_record[0].update({
            'service': self.service_ids.mapped("name"),
            'Facility': self.facility_ids.mapped("name"),
            'Price': (self.list_price, self.currency_id.symbol) if self.currency_id.position == 'after' else (self.currency_id.symbol, self.list_price),
            "room_variant_data": room_variant_data.read(['display_name'])
        })
        return room_record

    # -------------------------------------------------------------------------
    # CONSTRAINT METHODS
    # -------------------------------------------------------------------------

    @api.constrains('max_adult')
    def _check_max_adult(self):
        for record in self:
            if record.max_adult < 1:
                raise UserError("Adult must be 1 or more than...")


class ProductProduct(models.Model):

    """_summary_

    Parameters
    ----------
    models : model

    """

    _inherit = "product.product"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    is_room_booked = fields.Boolean("Is Room Booked", default=False)


class ProductAttribute(models.Model):

    """_summary_

    Parameters
    ----------
    models : model
    """

    _inherit = "product.attribute"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    website_visible = fields.Boolean("Is Visible on Website", default=True)
