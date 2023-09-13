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
from datetime import date, datetime

# Odoo Module
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteShopInherit(WebsiteSale):

    # -------------------------------------------------------------------------
    # OVERRIDE CONTROLLERS
    # -------------------------------------------------------------------------

    @http.route()
    def shop_payment(self, **post):
        res = super(WebsiteShopInherit, self).shop_payment(**post)
        sale_order = request.website.sale_get_order()
        order_line = sale_order.order_line
        for line in order_line:
            if line.product_id.product_tmpl_id.is_room_type:
                if not line.guest_info_ids:
                    return request.redirect("/guest/page")
        return res

    @http.route()
    def checkout(self, **post):
        res = super(WebsiteShopInherit, self).checkout(**post)
        sale_order = request.website.sale_get_order()
        room_type_product = (sale_order.order_line).filtered(
            lambda r: r if r.product_id.product_tmpl_id.is_room_type else None)
        if room_type_product and room_type_product.filtered(lambda r: r.guest_info_ids is False):
            return request.redirect("/guest/page")
        return res

    @http.route()
    def shop(self, page=0, category=None, min_price=0.0, max_price=0.0, search='', ppg=False, **post):
        request.session['check_in'] = post.get('check_in', False)
        request.session['check_out'] = post.get('check_out', False)
        return super(WebsiteShopInherit, self).shop(
            page=page, category=category, min_price=min_price, max_price=max_price, search=search, ppg=ppg, **post)

    @http.route()
    def cart(self, access_token=None, revive='', **post):
        sale_order = request.website.sale_get_order()
        if (sale_order.order_line.product_id).filtered('product_tmpl_id.is_room_type') and not sale_order.hotel_check_in:
            sale_order.is_room_type = True
        return super(WebsiteShopInherit, self).cart(
            access_token=access_token, revive=revive, **post)

    @http.route()
    def product(self, product, category='', search='', **kwargs):
        res = super(WebsiteShopInherit, self).product(
            product, category=category, search=search, **kwargs)
        check_in = request.session.get('check_in', False)
        check_out = request.session.get('check_out', False)
        if check_in and check_out:
            res.qcontext.update({
                'check_in_cart': datetime.strptime(check_in, '%Y-%m-%d'),
                'check_out_cart': datetime.strptime(check_out, '%Y-%m-%d'),
            })
        return res

    # -------------------------------------------------------------------------
    # CUSTOM CONTROLLERS
    # -------------------------------------------------------------------------

    @http.route('/get/website/room', type='json', auth='public', website=True)
    def get_room(self):
        website_id = request.website
        product_ids = website_id.website_homepage_product_ids
        pricelist = website_id.get_current_pricelist()
        room_template = request.env['ir.ui.view']._render_template("hotel_management_system.home_rooms", {
            'product_ids': product_ids,
            'website': website_id,
            'pricelist': pricelist
        })
        return room_template

    @http.route(['/empty/cart'], type='json', auth="public", website=True)
    def empty_cart(self, **kw):
        sale_order = request.website.sale_get_order()
        sale_order.order_line = False

    @http.route(['/available/qty/details'], type='json', auth="public", website=True)
    def cal_room_availability(self, requirement_qty='', product_template_id='', check_in='', check_out='', availabilty_check=''):
        if requirement_qty and product_template_id:
            sale_order = request.website.sale_get_order(force_create=True)
            check_in_val = datetime.strptime(check_in, '%Y-%m-%d')
            check_out_val = datetime.strptime(check_out, '%Y-%m-%d')
            if sale_order.order_line:
                if (sale_order.hotel_check_in and sale_order.hotel_check_out) and ((sale_order.hotel_check_in).date() != (check_in_val).date() or (sale_order.hotel_check_out).date() != (check_out_val).date()):
                    return {'result': 'unmatched'}
            else:
                sale_order.hotel_check_in = check_in
                sale_order.hotel_check_out = check_out

            product_template = request.env['product.template'].sudo().browse(
                int(product_template_id))
            total_room = product_template.product_variant_ids

            total_booking = request.env['hotel.booking'].sudo().search(
                [('status_bar', 'not in', ['initial', 'checkout'])])
            added_cart_room = 0
            for room in total_room:
                not_available = False
                if room.id not in (sale_order.mapped('order_line.product_id')).ids:
                    for booking in total_booking:
                        if room.id in (booking.mapped('booking_line_ids.product_id')).ids:
                            booking_check_in = booking.check_in
                            booking_check_out = booking.check_out
                            if booking.filter_booking_based_on_date(check_in_val, check_out_val):
                                not_available = True
                                break
                            else:
                                added_cart_room += 1
                                room_id = room
                                if availabilty_check == '0':
                                    request.env['sale.order.line'].create({
                                        'name': room_id.name+'('+check_in+' ' + check_out+')',
                                        'product_id': room_id.id,
                                        'product_uom_qty': (check_out_val.date() - check_in_val.date()).days or 1,
                                        'price_unit': room_id.currency_id._convert(room_id.list_price, sale_order.pricelist_id.currency_id, room_id.product_tmpl_id._get_current_company(pricelist=sale_order.pricelist_id), date.today()),
                                        'order_id': sale_order.id,
                                    })
                                break

                    # if room not in booking list
                    if room.id not in (sale_order.mapped('order_line.product_id')).ids and not_available is False:
                        added_cart_room += 1
                        room_id = room
                        if availabilty_check == '0':
                            request.env['sale.order.line'].sudo().create({
                                'name': room_id.name,
                                'product_id': room_id.id,
                                'product_uom_qty': (check_out_val.date() - check_in_val.date()).days or 1,
                                'price_unit': room_id.currency_id._convert(room_id.list_price, sale_order.pricelist_id.currency_id, room_id.product_tmpl_id._get_current_company(pricelist=sale_order.pricelist_id), date.today()),
                                'order_id': sale_order.id,
                            })

                    if added_cart_room == int(requirement_qty) and availabilty_check == '0':
                        return {'result': 'done', }
            if availabilty_check == '1' and added_cart_room:
                return {'result': 'done', 'tot_available_room': added_cart_room}

            if added_cart_room < int(requirement_qty):
                return {'result': 'fail'}


class GuestInfoController(http.Controller):

    # -------------------------------------------------------------------------
    # CUSTOM CONTROLLERS
    # -------------------------------------------------------------------------

    @http.route(['/guest/info'], type='json', auth="public", website=True)
    def discount(self, guest_detail='', **kw):
        for key, val in guest_detail.items():
            order_line_id = request.env['sale.order.line'].sudo().browse(
                int(key))
            order_line_id.guest_info_ids = False

            guest_info_data = [(0, 0, data) for data in val]
            order_line_id.write({'guest_info_ids': guest_info_data})


class GuestPageController(http.Controller):

    # -------------------------------------------------------------------------
    # CUSTOM CONTROLLERS
    # -------------------------------------------------------------------------

    @http.route('/guest/page', type='http', auth="public", website=True, csrf=False)
    def guest_info_page(self, **kw):
        sale_order = request.website.sale_get_order()
        if sale_order and sale_order.order_line.product_id.filtered('product_tmpl_id.is_room_type'):
            return request.render('hotel_management_system.guest_info_page')
        else:
            return request.redirect("/shop/cart")
