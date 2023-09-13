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
from odoo import fields,models


class HotelService(models.Model):
    """Services In room
        Parameters
        ----------
        models : Model
    """
    _name="hotel.service"
    _description="Hotel Services"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    name=fields.Char("Name")
    logo = fields.Binary('Logo')
    color = fields.Integer()

    #=== SQL CONSTRAINTS ===#

    _sql_constraints = [
     ('name_uniq','UNIQUE(name)', 'Service will unique always!!!'),]

