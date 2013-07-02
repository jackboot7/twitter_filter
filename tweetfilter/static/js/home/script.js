/*global $, document, window*/

$(document).ready(function () {

    $('#call_twitter_auth').click(function () {
        //window.location.href = "/auth/authenticate";
        var
            screen_name = $("#screen_name").val();

        window.open("/auth/authenticate/" + screen_name);
    });
});