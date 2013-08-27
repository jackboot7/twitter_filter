var
    update_retweets_status = function () {
        "use strict";

        $.get("/filtering/check_status/" + $('#current_channel').val(), function (data) {
            var
                btn = $('#switch_retweets_btn'),
                label = $('#switch_retweets_label');

            if(data.result === "enabled"){
                btn.attr('title', "Haga click para desactivar");
                label.text("Activo");
                label.removeClass('label-important').addClass('label-success');
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
            }
        });
    };

$(document).ready(function () {
    "use strict";

    update_retweets_status();

    $('#switch_retweets_btn').click(function () {
        $.post("/filtering/switch_status/" + $('#current_channel').val(), function (data) {
            update_retweets_status();
        });
    });
});
