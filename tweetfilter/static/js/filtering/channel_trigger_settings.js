var
    
    manage_linked_groups = function (group) {
               
        $.get("/filtering/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "Trigger"
        }, function (data) {
            $("#link_trigger_groups_select").multiselect("uncheckAll");        
            $("#link_trigger_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });
            $("#link_trigger_groups_select").multiselect("refresh");
        });
    },

    unlink_trigger_group = function(group_id) {
        $.post("/filtering/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_trigger_group_table();
        });
    },

    link_trigger_groups = function () {
        var checked_groups = $("#trigger_groups_select").val();

        $.post("/filtering/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "Trigger"
        }, function (data) {
            load_trigger_group_table();
        });
    },

    delete_trigger = function (trigger_id) {
        $.post("/filtering/trigger/delete/" + trigger_id, function (data) {
            if(data.result === "ok") {
                load_trigger_table(true);
            }
        });
    },

    load_trigger_table = function (exclusive) {
        "use strict";

        var delete_btn = "";

        $.get("/filtering/trigger/list/" + $('#viewing_trigger_group_id').val(), function (data) {
            $('#trigger_list_tbody').empty();

            if (data.length > 0) {
                $('#no_triggers_message').hide();
                $('#trigger_list_table').show();

                $.each(data, function (idx, elem) {
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_trigger_" + elem.id +"' class='no_decoration' " +
                            "title='Haga click para eliminar disparador'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                        $('#delete_trigger_header').show();
                        $('#add_trigger_btn_table').show();
                    } else {
                        delete_btn = "";                        
                        $('#delete_trigger_header').hide();
                        $('#add_trigger_btn_table').hide();
                    }

                    $('#trigger_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + delete_btn + "</td>" +
                        "</tr>"
                    );

                    if (exclusive) {
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
                    load_trigger_table(true);
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
        $('#viewing_trigger_group_id').val(group_id);
                
        load_trigger_table(exclusive);
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
                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_trigger_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#trigger_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_trigger_group_modal' data-toggle='modal' id='view_trigger_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_trigger_group_" + elem.id).click(function () {
                    view_trigger_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
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
    };

$(document).ready(function () {
    "use strict";

    load_trigger_group_table();

    
    $('#delete_trigger_confirmed').click(function () {
        $.post("/filtering/trigger/delete/" + $('#deleting_trigger_id').val(), function (data) {
            if(data.result === "ok") {
                load_trigger_table(true);
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

    $("#trigger_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_trigger_groups_btn').click(function () {
        manage_linked_groups();
    });

    $('#save_trigger_groups_btn').click(function () {
        link_trigger_groups();
    });
    
});