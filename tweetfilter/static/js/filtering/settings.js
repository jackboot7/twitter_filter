var
    /*
    trigger_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },*/

    submit_new_trigger = function () {
        "use strict";

        var trigger_text = $.trim($('#add_trigger_text').val());
        if(trigger_text.length > 0) {
            $.post("/filtering/trigger/add/", {
                'trigger_text': trigger_text,
                'group_id': $('#editing_trigger_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_trigger_text').val("");
                    load_trigger_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //trigger_add_error(data.result)
                }
            });
        }
    },

    load_trigger_table = function () {
        "use strict";

        $.get("/filtering/trigger/list/" + $('#editing_trigger_group_id').val(), function (data) {
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
                            "<td><a id='delete_trigger_" + elem.id +"' class='delete_trigger' " +
                            "title='Haga click para eliminar disparador'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    // ???????
                    $('#delete_trigger_' + elem.id).click(function () {
                        delete_trigger(elem.id);
                    });
                });

                $('#trigger_list_div').slimscroll();
            }else{
                $('#trigger_list_table').hide();
                $('#no_triggers_message').show();
            }
        });
    },

    edit_trigger_group = function (group) {
        "use strict";

        $('#trigger_group_modal_title').text("Editar grupo de disparadores");
        $('#editing_trigger_group_id').val(group.id);
        $('#add_trigger_group_name').val(group.name);

        load_trigger_table();
        // mostrar lista de triggers
    },

    load_trigger_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/filtering/trigger_group/list/", function (data) {
            $('#trigger_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_trigger_groups_message').hide();
                $('#trigger_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#trigger_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_trigger_group_btn_" + elem.id + "' href='#add_trigger_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#link_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_trigger_group_" + elem.id + "' class='delete_trigger_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_trigger_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_trigger_group_btn_' + elem.id).click(function () {
                        edit_trigger_group(elem);
                    });

                    $('#delete_trigger_group_' + elem.id).click(function () {
                        $('#deleting_trigger_group_id').val(elem.id);
                    });

                    // botón de asociar canales
                });
                $('#trigger_group_list_table').show();
            }else{
                $('#trigger_group_list_table').hide();
                $('#no_trigger_groups_message').show();
            }
        });
    },

    clear_add_trigger_group_form = function () {
        "use strict";

        $('#editing_trigger_group_id').val('');
        $('#add_trigger_group_name').val('');
    },

    trigger_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_trigger_group = function () {
        "use strict";

        var url;

        if ($('#editing_trigger_group_id').val() == "") {
            url = "/filtering/trigger_group/add/";
        }else{
            url = "/filtering/trigger_group/update/" + $('#editing_trigger_group_id').val();
        }

        $.post(url, {
            'trigger_group_name': $.trim($('#add_trigger_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_trigger_group_table();
                clear_add_trigger_group_form();
            }else{
                trigger_group_add_error(data.result);
            }
        });

    },

    validate_add_trigger_group_form = function () {
        "use strict";

        if($.trim($('#add_trigger_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_filtering_li').addClass("active");
    
    clear_add_trigger_group_form();
    load_trigger_group_table();

    $('#save_trigger_group_btn').click(function () {
        if(validate_add_trigger_group_form()){
            submit_trigger_group();
        }else{
            return false;
        }
    });

    $('#add_trigger_group_btn').click(function () {
        $('#trigger_group_modal_title').text("Crear grupo de disparadores");
        clear_add_hashtag_form();
    });

    $('#add_trigger_btn').click(function () {
        submit_new_trigger();
    });
});