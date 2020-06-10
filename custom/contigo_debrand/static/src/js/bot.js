
odoo.define('contigo_debrand.bot', function (require) {
    "use strict";

    var Message = require('mail.model.Message');

    Message.include({
        _getAuthorName: function () {
            if (this._isOdoobotAuthor()) {
                return "System";
            }
            return this._super.apply(this, arguments);
        },
    });
});
