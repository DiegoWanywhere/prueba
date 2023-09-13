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
from odoo import fields, models


#----------------- IN-ACTIVE ----------------#

class HotelManagement(models.Model):
    """Multi-Hotel

    Parameters
    ----------
    models : model
    """
    _name = "hotel.hotel"
    _description = "Hotel Management"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    name = fields.Char(string="Name",)
    logo = fields.Binary('Logo')
    hotel_description = fields.Text(
        string='Description', help='Brief managementrmation about Hotel')
    email = fields.Char(string="Email",related="contact_person.email")
    phone_no = fields.Char(string="Phone",related="contact_person.phone")
    mobile_no = fields.Char(string="Mobile",related="contact_person.mobile")
    website = fields.Char(string="Website Link")
    hotel_type_id = fields.Many2one(
        'hotel.type', string='Hotel Type')
    team_id = fields.Many2one(
        'crm.team', string='Sales team')
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State',
                               ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one(
        'res.country', string='Country', ondelete='restrict')
    branch = fields.Char("Branch")
    service_ids = fields.Many2many(
        'hotel.service', 'hotel_service_rel', 'hotel_id', 'service_id')
    facility_ids = fields.Many2many(
        'hotel.facility', 'hotel_facility_rel', 'hotel_id', 'facility_id')
    hotel_media_image_ids = fields.One2many(
        'hotel.media', 'hotel_image_id', string="Extra Product Media", copy=True)
    hotel_policies = fields.Text("Policy")
    hotel_check_in = fields.Datetime('Check In', required=False,
                                     help="Date of the arrival.")
    hotel_check_out = fields.Datetime('Check Out', required=False,
                                      help="Date of the departure.")
    contact_person = fields.Many2one('res.partner', string='Contact Person')


class HotelType(models.Model):
    """HOtel type

    Parameters
    ----------
    models : model
    """
    _name = "hotel.type"
    _description = "Hotel Type"
    _rec_name = "hotel_type"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    hotel_type = fields.Char("Hotel Type")
