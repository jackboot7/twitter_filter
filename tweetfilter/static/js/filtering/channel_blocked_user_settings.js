var
    
    validate_new_blocked_user = function () {
        "use strict";

        var text = $.trim($('#add_blocked_user_name').val());

        if (text.length == 0) {
            alert("Introduzca el nombre del usuario que desea bloquear");
            return false;
        }

        if (!(/^[a-zA-Z0-9_]{1,15}$/g).test(text)) {
            alert("El nombre del usuario no debe contener arroba (@) ni otros caracteres especiales");
            return false;
        }

        return true;
    },

    manage_linked_blocked_user_groups = function () {
               
        $.get("/filtering/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "BlockedUser"
        }, function (data) {
            $("#blocked_user_groups_select").multiselect("uncheckAll");        
            $("#blocked_user_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });
            $("#blocked_user_groups_select").multiselect("refresh");
        });
    },

    unlink_blocked_user_group = function(group_id) {
        $.post("/filtering/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_blocked_user_group_table();
        });
    },

    link_blocked_user_groups = function () {
        var checked_groups = $("#blocked_user_groups_select").val();

        $.post("/filtering/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "BlockedUser"
        }, function (data) {
            load_blocked_user_group_table();
        });
    },

    delete_blocked_user = function (blocked_user_id) {
        $.post("/filtering/blocked_user/delete/" + blocked_user_id, function (data) {
            if(data.result === "ok") {
                load_blocked_user_table(true);
            }
        });
    },

    load_blocked_user_table = function (exclusive) {
        "use strict";

        var delete_btn = "";

        $.get("/filtering/blocked_user/list/" + $('#viewing_blocked_user_group_id').val(), function (data) {
            $('#blocked_user_list_tbody').empty();

            if (data.length > 0) {
                $('#no_blocked_users_message').hide();
                $('#blocked_user_list_table').show();

                $.each(data, function (idx, elem) {
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_blocked_user_" + elem.id +"' class='no_decoration' " +
                            "title='Haga click para desbloquear el usuario'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                    } else {
                        delete_btn = "";                        
                    }

                    $('#blocked_user_list_tbody').append(
                        "<tr>" +
                            "<td>@" + elem.screen_name + "</td>" +
                            "<td>" + delete_btn + "</td>" +
                        "</tr>"
                    );

                    if (exclusive) {
                        $('#delete_blocked_user_' + elem.id).click(function () {
                            if (confirm("Está seguro de que desea desbloquear el usuario seleccionado?")) {
                                delete_blocked_user(elem.id);
                            }
                        });
                    }
                });
                $('#blocked_user_list_div').slimscroll();
            }else{
                $('#blocked_user_list_table').hide();
                $('#no_blocked_users_message').show();
            }
        });
    },

    submit_new_blocked_user = function () {
        "use strict";

        var blocked_user_text = $.trim($('#add_blocked_user_name').val());

        if (validate_new_blocked_user()) {
            $.post("/filtering/blocked_user/add/", {
                'blocked_user_name': blocked_user_text,
                'group_id': $('#viewing_blocked_user_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_blocked_user_name').val("");
                    load_blocked_user_table(true);
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //blocked_user_add_error(data.result)
                }
            });
        }
    },

    view_blocked_user_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_blocked_user_group_name').html(group_name);
        $('#viewing_blocked_user_group_id').val(group_id);
        
        if (exclusive) {
            $('#delete_blocked_user_header').show();
            $('#add_blocked_user_btn_table').show();
        } else {
            $('#delete_blocked_user_header').hide();
            $('#add_blocked_user_btn_table').hide();
        }

        load_blocked_user_table(exclusive);
    },

    load_blocked_user_group_table = function () {
        "use strict";

        $.get("/filtering/blocked_user_group/channel/"+$('#current_channel').val(), function (data) {
            $('#blocked_user_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_blocked_user_header').hide();
            } else {
                $('#unlink_blocked_user_header').show();
            }

            $('#blocked_user_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";
                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_blocked_user_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#blocked_user_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_blocked_user_group_modal' data-toggle='modal' id='view_blocked_user_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_blocked_user_group_" + elem.id).click(function () {
                    view_blocked_user_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
                    $('#delete_blocked_user_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_blocked_user_group(elem.id);
                        }
                    });
                }
            });

            $('#blocked_user_group_list_div').slimscroll();
        });
    },

    // Wat?
    blocked_user_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    };

$(document).ready(function () {
    "use strict";

    load_blocked_user_group_table();

    
    $('#delete_blocked_user_confirmed').click(function () {
        $.post("/filtering/blocked_user/delete/" + $('#deleting_blocked_user_id').val(), function (data) {
            if(data.result === "ok") {
                load_blocked_user_table(true);
            }
        });
    });

    $('#add_blocked_user_btn').click(function () {
        submit_new_blocked_user();
    });

    $('#add_blocked_user_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_blocked_user();
        }
    });

    $("#blocked_user_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_blocked_user_groups_btn').click(function () {
        manage_linked_blocked_user_groups();
    });

    $('#save_blocked_user_groups_btn').click(function () {
        link_blocked_user_groups();
    });
    
});