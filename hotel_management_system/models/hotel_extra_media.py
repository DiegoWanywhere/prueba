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

class HotelMedia(models.Model):
    """Store Hotel Media

    Parameters
    ----------
    models : Model
    """
    _name = "hotel.media"
    _description = "Hotel extra Media"

    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    hotel_image_id = fields.Many2one('hotel.hotel', "Hotel Gallery")
    hotel_gallery_image_ids = fields.One2many('product.image', 'hotel_image_id', string="Extra Product Media", copy=True)
    tags = fields.Text("Tags")
    category = fields.Text("Category")
