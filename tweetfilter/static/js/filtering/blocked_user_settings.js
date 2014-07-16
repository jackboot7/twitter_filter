var
    /*
    blocked_user_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },*/
    submit_channels = function () {
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/filtering/blocked_user_group/set_channels/" + $('#editing_blocked_user_group_id').val(), {
            'channels': JSON.stringify(checked_channels)
        }, function (data) {
            /*
            if (data.result == "OK") {
                // alert todo bien
            }
            */
        });
    },

    submit_new_blocked_user = function () {
        "use strict";

        if(!validate_new_blocked_user()){
            alert("El nombre de la cuenta no debe contener arroba (@) ni otros caracteres especiales");
            return false;
        }

        var blocked_user_text = $.trim($('#add_blocked_user_name').val());
        if(blocked_user_text.length > 0) {
            $.post("/filtering/blocked_user/add/", {
                'blocked_user_name': blocked_user_text,
                'group_id': $('#editing_blocked_user_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_blocked_user_name').val("");
                    load_blocked_user_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //blocked_user_add_error(data.result)
                }
            });
        }
    },

    delete_blocked_user = function (blocked_user_id) {
        $.post("/filtering/blocked_user/delete/" + blocked_user_id, function (data) {
            if(data.result === "ok") {
                load_blocked_user_table();
            }
        });
    },

    load_blocked_user_table = function () {
        "use strict";

        $.get("/filtering/blocked_user/list/" + $('#editing_blocked_user_group_id').val(), function (data) {
            $('#blocked_user_list_tbody').empty();

            if (data.length > 0) {
                $('#no_blocked_users_message').hide();
                $('#blocked_user_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#blocked_user_list_tbody').append(
                        "<tr>" +
                            "<td>@" + elem.screen_name + "</td>" +
                            "<td><a href='#' id='delete_blocked_user_" + elem.id +"' class='delete_blocked_user' " +
                            "title='Haga click para desbloquear usuario'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#delete_blocked_user_' + elem.id).click(function () {
                        delete_blocked_user(elem.id);
                    });
                });

                $('#blocked_user_list_div').slimscroll();
            }else{
                $('#blocked_user_list_table').hide();
                $('#no_blocked_users_message').show();
            }
        });
    },

    edit_blocked_user_group = function (group) {
        "use strict";

        $('#blocked_user_group_modal_title').text("Editar grupo de usuarios bloqueados");
        $('#editing_blocked_user_group_id').val(group.id);
        $('#add_blocked_user_group_name').val(group.name);
        $('#blocked_users_box').show();
        $('#save_blocked_user_group_btn').attr('data-dismiss', "modal");

        load_blocked_user_table();
        // mostrar lista de blocked_users
    },

    manage_linked_channels = function (group) {
        $('#editing_blocked_user_group_id').val(group.id);
        
        /*$.each(group.channels, function (index, value) {
            $("#link_channels_select").filter('[value="' + value + '"]').prop('selected', true);
        }); */
        
        $.get("/filtering/blocked_user_group/list_channels/" + group.id, {}, function (data) {
            $("#link_channels_select").multiselect("uncheckAll");        
            $("#link_channels_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });
            $("#link_channels_select").multiselect("refresh");
        });
    },

    delete_blocked_user_group = function () {
        $.post("/filtering/blocked_user_group/delete/" + $('#deleting_blocked_user_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_blocked_user_group_table();
            }
        });
    },

    load_blocked_user_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/filtering/blocked_user_group/list/", function (data) {
            $('#blocked_user_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_blocked_user_groups_message').hide();
                $('#blocked_user_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#blocked_user_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_blocked_user_group_btn_" + elem.id + "' href='#add_blocked_user_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a class='no_decoration' id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#add_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_blocked_user_group_" + elem.id + "' class='delete_blocked_user_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_blocked_user_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_blocked_user_group_btn_' + elem.id).click(function () {
                        edit_blocked_user_group(elem);
                    });

                    $('#delete_blocked_user_group_' + elem.id).click(function () {
                        $('#deleting_blocked_user_group_id').val(elem.id);
                    });

                    $('#link_channels_' + elem.id).click(function () {
                        manage_linked_channels(elem);
                    });
                });
            }else{
                $('#blocked_user_group_list_table').hide();
                $('#no_blocked_user_groups_message').show();
            }
        });
    },

    clear_add_blocked_user_group_form = function () {
        "use strict";

        $('#editing_blocked_user_group_id').val('');
        $('#add_blocked_user_group_name').val('');
        $('#blocked_users_box').hide();
        $('#save_blocked_user_group_btn').removeAttr("data-dismiss");
    },

    blocked_user_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_blocked_user_group = function () {
        "use strict";

        var 
            url,
            new_group = ($('#editing_blocked_user_group_id').val() == "")? true : false;

        if (new_group) {
            url = "/filtering/blocked_user_group/add/";
        }else{
            url = "/filtering/blocked_user_group/update/" + $('#editing_blocked_user_group_id').val();
        }

        $.post(url, {
            'blocked_user_group_name': $.trim($('#add_blocked_user_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_blocked_user_group_table();
                if(new_group){
                    edit_blocked_user_group(data.group_obj);
                }
            }else{
                if (data.result == "duplicate") {
                    alert("Ya existe un grupo con el nombre introducido");
                }
            }
        });

    },

    validate_new_blocked_user = function () {
        "use strict";

        return (/^[a-zA-Z0-9_]{1,15}$/g).test($('#add_blocked_user_name').val());
    },

    validate_add_blocked_user_group_form = function () {
        "use strict";

        if($.trim($('#add_blocked_user_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_filtering_li').addClass("active");
    
    clear_add_blocked_user_group_form();
    load_blocked_user_group_table();

    $('#save_blocked_user_group_btn').click(function () {
        if(validate_add_blocked_user_group_form()){
            submit_blocked_user_group();
        }else{
            return false;
        }
    });

    $('#add_blocked_user_group_btn').click(function () {
        $('#blocked_user_group_modal_title').text("Crear grupo de usuarios bloqueados");
        clear_add_blocked_user_group_form();
    });

    $('#add_blocked_user_btn').click(function () {
        submit_new_blocked_user();
    });

    $('#add_channels_modal').click(function () {
        /////
    });

    $('#save_channels_btn').click(function () {
        submit_channels();
    });

    $('#delete_blocked_user_group_confirmed').click(function () {
        delete_blocked_user_group();
    });

    $('#add_blocked_user_name').keypress(function (e) {
        if (e.which === 13) {
            submit_new_blocked_user();
        }
    });

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
    
});