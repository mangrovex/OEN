
odoo.define('contigo_debrand.web_client', function (require) {
"use strict";
    var WebClient = require('web.AbstractWebClient');
    
    WebClient.include({
        init: function(parent) {
            this._super.apply(this, arguments);
            var self = this;            
            self._rpc({
                model: "res.config.settings",
                method: 'get_debranding_settings',
            }, {
                shadow: true
            }).then(function(debranding_settings){
                odoo.debranding_settings = debranding_settings;
                self.set('title_part', {"zopenerp": odoo.debranding_settings.title_brand && odoo.debranding_settings.title_brand.trim() || ''});
            });
        }
    });

});