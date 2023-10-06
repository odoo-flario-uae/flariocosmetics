odoo.define("send_coupons.ValidateCouponsForm", function(require) {
    'use strict';
    var publicWidget = require("web.public.widget")

    publicWidget.registry.ValidateCouponsForm = publicWidget.Widget.extend({
        selector:"coupons_form",
        events: {
            "submit": "_onSubmitButton"
        },

        _onSubmitButton: function(evt) {
            evt.preventDefault();
            console.log("Hello this submit event");
        }
    })
})