var
    load_trigger_table = function () {
        "use strict";

        $.get("/filtering/trigger/list/"+$('#current_channel').val(), function (data) {
            $('#trigger_list_tbody').empty();

            if (data.length > 0) {
                $('#no_triggers_message').hide();
                $('#trigger_list_table').show();
                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {
                    //alert(elem.enabled_mentions);
                    $('#trigger_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            /*
                            "<td><div class='offset2'><input id='trigger_mention_check_" + elem.id +
                            "' type='checkbox'></div></td>" +
                            "<td><div class='offset1'><input id='trigger_dm_check_" + elem.id +
                            "' type='checkbox'></div></td>" +
                            */
                            "<td><a id='delete_trigger_" + elem.id +"' class='delete_trigger' " +
                            "title='Haga click para eliminar disparador' href='#delete_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    /*
                    $('#trigger_mention_check_' + elem.id).attr('checked', elem.enabled_mentions);
                    $('#trigger_dm_check_' + elem.id).attr('checked', elem.enabled_dm);

                    $('#trigger_mention_check_' + elem.id).change(function () {
                        $.post("/filtering/trigger/switch_mention/" + elem.id, function () {

                        });
                    });

                    $('#trigger_dm_check_' + elem.id).change(function () {
                        $.post("/filtering/trigger/switch_dm/" + elem.id, function () {

                        });
                    });
                    // */

                    $('#delete_trigger_' + elem.id).click(function () {
                        $('#deleting_trigger_text').text(elem.text);
                        $('#deleting_trigger_id').val(elem.id);
                    });
                });

                $('#trigger_list_div').slimscroll();
            }else{
                $('#trigger_list_table').hide();
                $('#no_triggers_message').show();
            }
        });
    },

    trigger_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_new_trigger = function () {
        "use strict";

        var trigger_text = $.trim($('#add_trigger_text').val());
        if(trigger_text.length > 0) {
            $.post("/filtering/trigger/add/", {
                'trigger_text': trigger_text,
                'trigger_channel': $('#current_channel').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_trigger_text').val("");
                    load_trigger_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    trigger_add_error(data.result);
                }
            });
        }
    };

$(document).ready(function () {
    "use strict";


    $('#trigger_list_table').hide();
    $('#no_triggers_message').hide();

    load_trigger_table();

    $('#delete_trigger_confirmed').click(function () {
        $.post("/filtering/trigger/delete/" + $('#deleting_trigger_id').val(), function (data) {
            if(data.result === "ok") {
                load_trigger_table();
            }
        });
    });

    $('#add_trigger_btn').click(function () {
        submit_new_trigger();
    });

    $('#add_trigger_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_trigger();
        }
    });
});