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
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.addons.website.tools import get_video_embed_code

#----------------- IN-ACTIVE ----------------#

class HotelImage(models.Model):
    """Hotel image module

    Parameters
    ----------
    models : model
    """
    _name = 'hotel.image'
    _description = "Hotel Image"
    _inherit = ['image.mixin']
    _order = 'sequence, id'


    # -------------------------------------------------------------------------//
    # MODEL FIELDS
    # -------------------------------------------------------------------------//

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    image_1920 = fields.Image(required=True)
    video_url = fields.Char('Video URL',
                            help='URL of a video for showcasing your product.')
    embed_code = fields.Char(compute="_compute_embed_code")
    can_image_1024_be_zoomed = fields.Boolean("Can Image 1024 be zoomed", compute='_compute_can_image_1024_be_zoomed', store=True)