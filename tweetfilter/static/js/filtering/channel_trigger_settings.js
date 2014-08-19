var
    unlink_trigger_group = function (group_id) {

    },

    link_new_group = function () {

    },

    submit_new_trigger = function () {
        "use strict";

        var trigger_text = $.trim($('#add_trigger_text').val());
        if(trigger_text.length > 0) {
            $.post("/filtering/trigger/add/", {
                'trigger_text': trigger_text,
                'group_id': $('#viewing_trigger_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_trigger_text').val("");
                    load_trigger_table();   //////////////////////////////////////
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //trigger_add_error(data.result)
                }
            });
        }
    },

    view_trigger_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_trigger_group_name').html(group_name);
        var delete_btn = "";
        
        if (exclusive == "true") {
            delete_btn = 
                "<a href='#' id='delete_trigger_" + elem.id +"' class='delete_trigger' " +
                "title='Haga click para eliminar disparador'>" +
                "<span class='badge badge-important' contenteditable='false'>x</span></a>";
            $('#delete_trigger_header').hide();
            $('#add_trigger_btn_table').show();
        } else {
            delete_btn = "";
            $('#delete_trigger_header').show();
            $('#add_trigger_btn_table').hide();
        }

        $.get("/filtering/trigger/list/" + group_id, function (data) {
            $('#trigger_list_tbody').empty();

            if (data.length > 0) {
                $('#no_triggers_message').hide();
                $('#trigger_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#trigger_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + delete_btn + "</td>" +
                        "</tr>"
                    );

                    if (exclusive != "true") {
                        $('#delete_trigger_' + elem.id).click(function () {
                            if (confirm("Está seguro de que desea eliminar el disparador seleccionado?")) {
                                delete_trigger(elem.id);
                            }
                        });
                    }
                });
                $('#trigger_list_div').slimscroll();
            }else{
                $('#trigger_list_table').hide();
                $('#no_triggers_message').show();
            }
        });
    },

    load_trigger_group_table = function () {
        "use strict";

        $.get("/filtering/trigger_group/channel/"+$('#current_channel').val(), function (data) {
            $('#trigger_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_trigger_header').hide();
            } else {
                $('#unlink_trigger_header').show();
            }

            $('#trigger_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";
                if (elem.channel_exclusive == "true")  {
                    unlink_button = 
                        "<a id='delete_trigger_group_" + elem.id +"' class='delete_trigger' " +
                        "title='Haga click para desvincular el grupo' href='#'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#trigger_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_trigger_group_modal' data-toggle='modal' id='view_trigger_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_trigger_group_" + elem.id).click(function () {
                    view_trigger_group_(elem.id, elem.name, elem.channel_exclusive);
                });

                if (elem.channel_exclusive != "true") {
                    $('#delete_trigger_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_trigger_group(elem.id);
                        }
                    });
                }
            });

            $('#trigger_group_list_div').slimscroll();
        });
    },

    // Wat?
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

    load_trigger_group_table();

    /*
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
    */
});