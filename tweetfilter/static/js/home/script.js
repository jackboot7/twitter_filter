/*global $, document, window, alert*/

var
    load_channel_table = function () {
        "use strict";
        $.get("/channels/list", function (data) {
            if (data.length > 0) {
                // populate table
            }
        });
    };

$(document).ready(function () {
    load_channel_table();

    $('#call_twitter_auth').click(function () {
        var
            screen_name = $("#screen_name").val();

        window.location.href = "/auth/authenticate/" + screen_name;
        //window.open("/auth/authenticate/" + screen_name);

    });
});