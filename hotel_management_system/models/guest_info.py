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
import logging

#Odoo Module
from odoo import fields, models, api
_log = logging.getLogger(__name__)


class GuestInfo(models.Model):
    """Module to manage Guest Information

    Parameters
    ----------
    models : importing Model
    """
    _name = "guest.info"
    _description = "Guest Information"
     # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    name = fields.Char('Name')
    sale_order_line_id=fields.Many2one('sale.order.line')
    booking_id=fields.Many2one('hotel.booking.line')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    age = fields.Integer('Age')
