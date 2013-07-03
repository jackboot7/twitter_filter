/*global $, document, window*/

$(document).ready(function () {

    $('#call_twitter_auth').click(function () {
        var
            screen_name = $("#screen_name").val();

        window.location.href = "/auth/authenticate/" + screen_name;
        //window.open("/auth/authenticate/" + screen_name);

    });
});