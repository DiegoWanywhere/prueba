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
{
    "name": "A complete Hotel Management Solution in ODOO",
    "summary": "Odoo hotel management by webkul Book rooms, room reservation, manage hotel booking, paid services, book hotels rooms, pos restraurant, motel, holiday, mmt, indigo, travigo",
    "author":  "Webkul Software Pvt. Ltd.",
    "depends": ['account', 'sale_management', 'website_sale', 'website', 'wk_wizard_messages'],
    "category":  "website",
    "version":  "1.1.8",
    "sequence":  1,
    "license":  "Other proprietary",
    "website":  "https://store.webkul.com/odoo-hotel-management-system.html",
    "description":  "Odoo Hotel Management Module enables you to manage rooms of a hotel or other lodging facilities. Admin can also add bookings from the Odoo backend.",
    "live_test_url":  "https://odoodemo.webkul.com/demo_feedback?module=hotel_management_system",
    "data": [
        "security/ir.model.access.csv",
        "report/booking_report.xml",
        "report/booking_report_templates.xml",
        "wizard/exchange_room_views.xml",
        "wizard/compute_bill_views.xml",
        "wizard/add_booking_room_views.xml",
        "wizard/attached_doc_views.xml",
        "views/hotel_booking_views.xml",
        "views/hotel_management_views.xml",
        "views/hotel_booking_line_views.xml",
        "views/hotel_extra_media_views.xml",
        "views/hotel_service_views.xml",
        "views/hotel_facility_views.xml",
        "views/product_views.xml",
        "views/template.xml",
        'views/snippets/hotel_room_snippet.xml',
        'views/snippets/snippets.xml',
        "views/variant.xml",
        "views/room_service_views.xml",
        "views/sale_order_views.xml",
        "views/account_view.xml",
        'views/res_config_settings_views.xml',
    ],
    'demo': [
        'data/hotel_demo.xml',
    ],
    "images":  ['static/description/banner.gif'],
    "assets": {
        'web.assets_frontend': [
            "hotel_management_system/static/src/scss/style.scss",
            "hotel_management_system/static/src/snippets/s_hotel/000.scss",
            "hotel_management_system/static/src/snippets/s_hotel/000.js",
            "hotel_management_system/static/src/js/available_rooms.js",
        ],
        'web.assets_backend': [
            'hotel_management_system/static/src/views/**/*',
            'hotel_management_system/static/src/scss/dashboard.scss',
        ]
    },
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  299,
    "currency":  "USD",
    "pre_init_hook":  "pre_init_check",
}
