odoo.define('bi_website_free_delivery_info.free_delivery_info', function (require) {
'use strict';

var core = require('web.core');
var _t = core._t;
var delivery = require('website_sale_delivery.checkout');
var publicWidget = require('web.public.widget');
var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var rpc = require('web.rpc');

publicWidget.registry.websiteSaleDelivery.include({


    _handleCarrierUpdateResultBadge: function (result) {
        var def = this._super.apply(this, arguments);
        $('#cart_total').find('.success').empty();
        var order_id = $('input[name="website_sale_order"]').val();
        $('.offer').show();
        rpc.query({
            model: 'sale.order',
            method: 'search_read',
            domain: [['id','=', parseInt(order_id)],['carrier_id','=', parseInt(result.carrier_id)]]
        }).then(function(data){
            var amount_remain = result.buy_more_amount
            $('.buy_more_amount').text(amount_remain)            
            if(result.is_free_delivery){
                if(data.length > 0){
                    var $freedeliveryinfo = $('#cart_total').find('.success')
                    var success_msg = $($freedeliveryinfo).html("<p class='btn btn-success'>Congratulations , You have won FREE DELIVERY on this order</p>")
                    $('.offer').hide();
                }
            }

        })
        return def;
    },

})

publicWidget.registry.OfferPopup = publicWidget.Widget.extend({
    selector: '#wrapwrap',


    events: {
        'click #info_btn': '_show_popover',
    },

    _show_popover: function(ev) {
        var delivery_id = $(ev.currentTarget).attr('data-id');

        ajax.jsonRpc('/shiiping_method/check', 'call', { 
            'delivery_id' :  parseInt(delivery_id)
        }).then(function(data){
            var offer_message = $('.info-hover').html("<div class='d-none'>Place a order of minimum <b>"+ data.currency +" </b>to get <br/>FREE DELIVERY!<br></div>")

            if(data && data.free_delivery == true){
                $('.info-btn-offer_'+parseInt(delivery_id)+'').popover({content : offer_message[0],
                    placement: 'right',
                    container: 'body',
                });
                $('.info-btn-offer_'+parseInt(delivery_id)+'').popover('show');
            }
        });
    }
})

});