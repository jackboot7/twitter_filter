var

    load_timeblock_table = function () {
        "use strict";

        $.get("/channels/timeblock/list/"+$('#current_channel').val(), function (data) {
            $('#timeblock_list_tbody').empty();

            if (data.length > 0) {
                $('#no_timeblocks_message').hide();
                $('#timeblock_list_table').show();
                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {
                    /*
                    $('#timeblock_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td><a id='delete_timeblock_" + elem.id +"' class='delete_filter' " +
                            "title='Haga click para eliminar filtro' href='#delete_filter_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#delete_filter_' + elem.id).click(function () {
                        $('#deleting_filter_text').text(elem.text);
                        $('#deleting_filter_id').val(elem.id);
                    });
                    */
                });
            }else{
                $('#timeblock_list').hide();
                $('#no_timeblocks_message').show();
            }
        });
    },

    timeblock_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_new_timeblock = function () {
        "use strict";

        $.post("/channels/timeblock/add/", {
            /*
            'start': $('#').val(),
            'end': $('#').val()
            */
        }, function (data) {

            if(data.result === "ok") {
                load_timeblock_table();
            }else{
                timeblock_add_error(data.result);
            }
        });
    };

$(document).ready(function () {
    "use strict";

    $('#timeblock_list').hide();
    $('#no_timeblocks_message').hide();

    load_timeblock_table();

    $('#delete_timeblock_confirmed').click(function () {
        $.post("/channels/timeblock/delete/" + $('#deleting_timeblock_id').val(), function (data) {
            if(data.result === "ok") {
                load_timeblock_table();
            }
        });
    });

    $('#add_timeblock_btn').click(function () {
        submit_new_timeblock();
    });
});