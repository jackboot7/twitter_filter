/*global $, document, window, alert*/

var
    load_channel_table = function () {
        var
            row_class,
            label_span;

        $.get("/channels/list", function (data) {
            if (data.length > 0) {
                $('#no_channels_message').hide();
                $('#channel_list_table').show();

                $.each(data, function (idx, elem){
                    row_class = (elem.status === "Activo")?
                        "success" :
                        "error";
                    label_span = (elem.status === "Activo")?
                        "<span class='label label-success'>" :
                        "<span class='label label-important'>";

                    $('#channel_list_tbody').append("<tr class='" + row_class + "'>"+
                        "<td><a href='#'>" + elem.screen_name + "</a></td>" +
                        "<td>" + elem.last_tweet + "</td>" +
                        "<td><a title='Haga click para desactivar' class='channel_row' id='' href='#'>" +
                        label_span + elem.status + "</span></a></td>" +
                        "<td><a id='delete_channel_" + elem.screen_name +"' class='delete_channel' " +
                        "title='Haga click para eliminar canal' href='#delete_confirm_modal' data-toggle='modal'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td></tr>");

                    $('#delete_channel_' + elem.screen_name).click(function () {
                        $('#deleting_channel_id').text(elem.screen_name);
                    });
                });
            }else{
                $('#channel_list_table').hide();
                $('#no_channels_message').show();
            }
        });
    },

    channel_add_success = function () {
        $('#alert_success_body').text("El canal fue suscrito exitosamente.");
        $('#alert_success').show();
    },

    channel_delete_success = function () {
        $('#alert_success_body').text("El canal fue eliminado exitosamente.");
        $('#alert_success').show();
    };


$(document).ready(function () {
    $('#channel_list_table').hide();
    $('#no_channels_message').hide();

    load_channel_table();

    $('#call_twitter_auth').click(function () {
        var
            screen_name = $("#screen_name").val();

        window.location.href = "/auth/authenticate/";
        //window.open("/auth/authenticate/" + screen_name);

    });

    $('#delete_channel_confirmed').click(function () {
        $.post("/channels/delete/" + $('#deleting_channel_id').text(), function (data) {
            if(data.result === "ok") {
                channel_delete_success();
                load_channel_table();
            }
        });
    });
});