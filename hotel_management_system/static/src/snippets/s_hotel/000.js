/** @odoo-module **/

import * as publicWidget from 'web.public.widget'

publicWidget.registry.rooms = publicWidget.Widget.extend({
    selector: '.selectiveRoomforhomePage',
    disabledInEditableMode: false,
    start: function () {
        var self = this;
        self._empty_$el();

        // -------------------------------------------------------------------------
        // Add spinner
        // -------------------------------------------------------------------------
        self.$el.append('<div class="d-flex justify-content-center"><div class="lds-hourglass"></div></div>')

        self._rpc({
            route: "/get/website/room",
        }).then(function (data) {
            setTimeout(function () {
                self._empty_$el();
                self.$el.append(data)
            }, 500);
        });
    },

    //Empty to snippet div
    _empty_$el() {
        this.$el.empty();
    }
});
