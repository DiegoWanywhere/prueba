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
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'


    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//
    booking_count = fields.Integer('Booking count', copy = False)

    # -------------------------------------------------------------------------
    # OPEN VIEWS
    # -------------------------------------------------------------------------
    def action_view_source_booking(self):
        self.ensure_one()
        source_orders = self.line_ids.sale_line_ids.order_id
        if self.sale_order_count == 1:
            return source_orders.action_view_booking()
