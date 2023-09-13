odoo.define('hotel_managememnt_system.available_rooms', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0');
    var yyyy = today.getFullYear();
    today = yyyy + '-' + mm + '-' + dd;
    $("#wk_check_in").prop("min", today);
    $('#wk_check_out').on('click', function () {
        if ($("#wk_check_in").val()) {
            var check_in_val = $("#wk_check_in").val();
            var currentCheckin = new Date(check_in_val);
            currentCheckin.setDate(currentCheckin.getDate() + 1);
            var formatted_checkoutDate = JSON.stringify(currentCheckin);
            $(this).prop("min", formatted_checkoutDate.slice(1, 11));
        }
    });
    $("#check_in_cart").prop("min", today);
    $('#check_in_cart').on('change', function () {
        if (Date.parse($("#check_in_cart").val()) >= Date.parse($("#check_out_cart").val())) {
            $("#check_out_cart").val(null);
        }
    });
    $('#check_out_cart').on('click', function () {
        if ($("#check_in_cart").val()) {
            var check_in_val = $("#check_in_cart").val();
            var currentCheckin = new Date(check_in_val);
            currentCheckin.setDate(currentCheckin.getDate() + 1);
            var formatted_checkoutDate = JSON.stringify(currentCheckin);
            $(this).prop("min", formatted_checkoutDate.slice(1, 11));
        }
    });
    $(document).ready(function () {
        $('.add_Guest_span').on('click', function () {
            $('#addguestModalCenter').modal('show');
            var table_id = $(this).parent('div').parent('div').children('table').attr('id');

            $('.table_id_store').val(table_id);
            console.log('------------------', $('.table_id_store').val(table_id).val());
        })
        $('.addGuestModal_button').on('click', function () {
            var newGuest_info;
            var fullName = $('.fullName').val();
            var genderValue = $("input[name='genderinlineRadioOptions']:checked").val();
            var age = $('.age').val();
            var table_id_store = $('.table_id_store').val();
            console.log('------------------', table_id_store);
            if (fullName && genderValue && age && table_id_store) {
                // var tableid = $('#' + table_id_store);
                var desire_table = $('#accordionGuest').find("table#" + table_id_store);
                console.log('------------------', desire_table.attr('id'));
                var tbody_val = desire_table.children('tbody');
                var tbody_div = tbody_val.first();
                var select_option;
                if (genderValue == "male") {
                    select_option = '<option value="male" selected>Male</option><option value="female">Female</option>';
                }
                else {
                    select_option = '<option value="male">Male</option><option value="female" selected>Female</option>';
                }

                tbody_div.append(`<tr>
        <td>
                <input class = "form-control" type="text" name="name" value=`+ fullName + ` required="True"/>
        </td>
        <td>
                <select class = "form-control" name="gender" id="gender" required="True">
                `+ select_option + `
                </select>
        </td>
        <td>
                <input class = "form-control" type="number" value=`+ age + ` name="age" required="True"/>
        </td>
        <td>
            <span type="button" id="remove_row" class="btn mt-2 mb-2 btn-danger btn-sm inline remove_row">Remove</span>
        </td>
    </tr>`);
                $('#addguestModalCenter').modal('hide');
            }
        })
        $('.guest_info_body').on('click', '.remove_row', function () {
            console.log('--------------------', $(this));
            var tbody_val = $(this).parent('td').parent('tr').parent('tbody');
            console.log('--------------------', $(this).parent('td').parent('tr'));
            if (tbody_val.children('tr').length > 1) {
                $(this).closest('tr').remove();
            }


            // console.log('--------------------', $(this).closest('tr'));

        });
        $('#wk_check_in').on('change', function () {
            if (Date.parse($("#wk_check_in").val()) >= Date.parse($("#wk_check_out").val())) {
                $("#wk_check_out").val(null);
            }
        });
        $('#submit_detail').on('click', function () {
            var info_dict = {};


            var check_point = 0;
            $('.outer_div').each(function () {
                var max_child = 0;
                var max_adult = 0;
                var total_adult = 0;
                var total_child = 0;
                var line_id = $(this).attr('id');
                max_adult = $(this).find('.max_adult').val();
                max_child = $(this).find('.max_child').val();

                // var room_name = $(this).find('.room_name').val();

                var data_list = [];
                $(this).children('table').children('tbody').find('tr').each(function (i, el) {

                    var $tds = $(this).find("td");

                    var dict = {};
                    $tds.each(function (j, val) {
                        if ($(this).children().attr('type') == "number") {
                            if ($(this).children().val() > 12) {
                                total_adult += 1;
                            }
                            else {
                                total_child += 1;
                            }

                        }
                        if (!$(this).children().val() && !($(this).children().attr('type') == "button")) {
                            check_point = 1
                            $("#data_missing").css("display", "none");
                            $('#data_missing').css("display", "block");
                        }
                        else {
                            if (!($(this).children().attr('type') == "button")) {
                                dict[$(this).children().attr('name')] = $(this).children().val();
                            }

                        }

                    });
                    if (max_adult < total_adult || max_child < total_child) {
                        check_point = 2
                    }
                    data_list.push(dict);
                });
                info_dict[line_id] = data_list;
            });
            if (check_point == 2) {
                // console.log('--------------------', total_adult, total_child);

                $("#acceptable_guest").css("display", "none");
                $('#acceptable_guest').css("display", "block");

            }

            else if (check_point == 0) {
                ajax.jsonRpc('/guest/info', 'call', { 'guest_detail': info_dict }).then(function (val) {
                    window.location = '/shop/checkout?express=1';
                });

            }

        });
    });
    // $('#check_availability').on('click', function () {
    //     if ($('#check_in_cart').val() && $('#check_out_cart').val()) {
    //         $("#caution_date").css("display", "none");
    //         var check_in = $('#check_in_cart').val();
    //         var check_out = $('#check_out_cart').val();
    //         var product_template_id = $('input[name="product_template_id"]').val();
    //         var requirement_qty = $('input[name="add_qty"]').val();
    //         ajax.jsonRpc('/available/qty/details', 'call', { 'check_in': check_in, 'check_out': check_out, 'product_template_id': product_template_id, 'requirement_qty': requirement_qty, 'availabilty_check': '1' }).then(function (val) {
    //             if (val['result'] == 'done') {
    //                 console.log('------ava-----------', val['tot_available_room']);
    //                 $('.tot_available_room').text(val['tot_available_room']);
    //                 $(".msg_alert").css("display", "none");
    //                 $("#available_room").css("display", "block");
    //             }
    //             else if (val['result'] == 'unmatched') {
    //                 $('#modalAbandonedCart').modal('show');
    //             }
    //             else {
    //                 $(".msg_alert").css("display", "none");
    //                 $("#caution_msg").css("display", "block");

    //             }
    //         });
    //     }
    //     else {
    //         $(".msg_alert").css("display", "none");
    //         $("#caution_date").css("display", "block");
    //     }
    // });
    $('.emptyCart').on('click', function () {
        ajax.jsonRpc('/empty/cart', 'call', {}).then(function () {
            location.reload();
        });
    });

    $(document).on('click', '#check_booking_room_availability', function () {
        if ($('#check_in_cart').val() && $('#check_out_cart').val()) {
            $("#caution_date").css("display", "none");
            var check_in = $('#check_in_cart').val();
            var check_out = $('#check_out_cart').val();
            var product_template_id = $('input[name="product_template_id"]').val();
            var product_varient_id = $('input[name="product_id"]').val();
            var requirement_qty = $('input[name="add_qty"]').val() || 1;
            ajax.jsonRpc('/available/qty/details', 'call', { 
                'check_in': check_in, 
                'check_out': check_out, 
                'product_template_id': product_template_id, 
                'requirement_qty': requirement_qty, 
                'availabilty_check': '0',
                'product_varient_id': product_varient_id })
            .then(function (val) {

                if (val['result'] == 'fail') {
                    $(".msg_alert").css("display", "none");
                    $("#caution_msg").css("display", "block");




                }
                else if (val['result'] == 'unmatched') {
                    $('#modalAbandonedCart').modal('show');
                    // $(".msg_alert").css("display", "none");
                    // $("#caution_date_mismatched").css("display", "block");
                }
                else {
                    // $("#available_room").css("display", "none");
                    $(".msg_alert").css("display", "none");
                    $("#success_msg").css("display", "block");
                    setTimeout(function () { window.location = '/shop/cart'; }, 1000);

                }

            });
        }
        else {
            $(".msg_alert").css("display", "none");
            $("#caution_date").css("display", "block");
        }
    });
});