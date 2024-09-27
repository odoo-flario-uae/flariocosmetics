odoo.define('website_first_order_discount.editor', function (require) {
'use strict';
var getCookie = require("web.utils.cookies");
var ajax = require('web.ajax');
    ajax.jsonRpc("/shop/user_orders","call",{}).then(function(obj) {
        if (obj) {
            console.log(obj)
        }
    });


	if (window.location.pathname == '/shop') {
//        debugger
		if( getCookie.getCookie('modalShown') === '' )  {
            ajax.jsonRpc("/shop/disc_popup","call",{}).then(function(obj) {
                if (obj) {
                    var modal = $(obj);
                    $('#wrap').append(modal);
                    modal.find('.modal').modal('show');
                    getCookie.setCookie('modalShown', true)
                }
            });
        }

	}

})
