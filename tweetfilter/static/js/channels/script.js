var
    load_trigger_table = function () {
        "use strict";

        $.get("/filtering/trigger/list", function (data) {
            $('#trigger_list_tbody').empty();

            if (data.length > 0) {
                $('#no_triggers_message').hide();
                $('#trigger_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#channel_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + elem.get_action_display + "</td>" +
                            "<td><a id='delete_trigger_" + elem.id +"' class='delete_trigger' " +
                            "title='Haga click para eliminar disparador' href='#delete_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#delete_trigger_' + elem.id).click(function () {
                        $('#deleting_trigger_text').text(elem.text);
                    });
                });
            }else{
                $('#trigger_list_table').hide();
                $('#no_triggers_message').show();
            }
        });
    };

$(document).ready(function () {
    "use strict";

    $('#trigger_list_table').hide();
    $('#no_triggers_message').hide();

    load_trigger_table();

    $('#delete_trigger_confirmed').click(function () {
        $.post("/filtering/trigger/delete/" + $('#deleting_trigger_text').text(), function (data) {
            if(data.result === "ok") {
                load_trigger_table();
            }
        });
    });
});