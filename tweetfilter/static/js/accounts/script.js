/*global $, document, window, alert*/

var
    
    load_channel_table = function () {
        "use strict";

        var
            row_class,
            label_class,
            link_title;

        $.get("/accounts/list", function (data) {
            $('#channel_list_tbody').empty();

            if (data.length > 0) {
                $('#no_channels_message').hide();
                $('#channel_list_table').show();

                $.each(data, function (idx, elem){
                    $('#channel_list_tbody').append(
                        "<tr id='channel_row_" + elem.screen_name + "'>"+
                        "<td><a href='/filtering/edit/" + elem.screen_name + "/'>" + elem.screen_name + "</a></td>" +
                        "<td>" + elem.filtering + "</td>" +
                        "<td>" + elem.scheduling + "</td>" +
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
        "use strict";

        $('#alert_success_body').text("El canal fue suscrito exitosamente.");
        $('#alert_success').show();
    },

    channel_delete_success = function () {
        "use strict";

        $('#alert_success_body').text("El canal fue eliminado exitosamente.");
        $('#alert_success').show();
    };


$(document).ready(function () {
    "use strict";

    //$('#channel_list_table').hide();
    $('#no_channels_message').hide();

    if($('#channel_added').val() === "true") {
        channel_add_success();
    }

    //load_channel_table();

    $('#call_twitter_auth').click(function () {
        var
            screen_name = $("#screen_name").val();

        window.location.href = "/accounts/authenticate/";

    });

    $('#delete_channel_confirmed').click(function () {
        $.post("/accounts/delete/" + $('#deleting_channel_id').text(), function (data) {
            if(data.result === "ok") {
                channel_delete_success();
                load_channel_table();
            }
        });
    });

    $('.delete_channel').each(function (index) {
        var name = $(this).attr('id');
        $(this).click(function () {
            $('#deleting_channel_id').text(name.substr(15));
        });
    });

});
