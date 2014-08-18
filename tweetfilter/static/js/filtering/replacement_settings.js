var
    
    submit_channels = function () {
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/filtering/replacement_group/set_channels/" + $('#editing_replacement_group_id').val(), {
            'channels': JSON.stringify(checked_channels)
        }, function (data) {
            /*
            if (data.result == "OK") {
                // alert todo bien
            }
            */
        });
    },

    submit_new_replacement = function () {
        "use strict";

        var replacement_text = $.trim($('#add_replacement_text').val());
        if(replacement_text.length > 0) {
            $.post("/filtering/replacement/add/", {
                'replacement_text': replacement_text,
                'replacement_replace_with' : $('#add_replacement_replace_with').val(),
                'group_id': $('#editing_replacement_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_replacement_text').val("");
                    $('#add_replacement_replace_with').val("");
                    load_replacement_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                }
            });
        }
    },

    delete_replacement = function (replacement_id) {
        $.post("/filtering/replacement/delete/" + replacement_id, function (data) {
            if(data.result === "ok") {
                load_replacement_table();
            }
        });
    },

    load_replacement_table = function () {
        "use strict";

        $.get("/filtering/replacement/list/" + $('#editing_replacement_group_id').val(), function (data) {
            $('#replacement_list_tbody').empty();

            if (data.length > 0) {
                $('#no_replacements_message').hide();
                $('#replacement_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#replacement_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + elem.replace_with + "</td>" +
                            "<td><a href='#' id='delete_replacement_" + elem.id +"' class='delete_replacement' " +
                            "title='Haga click para eliminar supresor'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#delete_replacement_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea eliminar el supresor seleccionado?")) {
                            delete_replacement(elem.id);
                        }
                    });
                });

                $('#replacement_list_div').slimscroll();
            }else{
                $('#replacement_list_table').hide();
                $('#no_replacements_message').show();
            }
        });
    },

    edit_replacement_group = function (group) {
        "use strict";

        $('#replacement_group_modal_title').text("Editar grupo de supresores");
        $('#editing_replacement_group_id').val(group.id);
        $('#add_replacement_group_name').val(group.name);
        $('#replacements_box').show();
        $('#save_replacement_group_btn').attr('data-dismiss', "modal");

        load_replacement_table();
    },

    manage_linked_channels = function (group) {
        $('#editing_replacement_group_id').val(group.id);
        
        $.get("/filtering/replacement_group/list_channels/" + group.id, {}, function (data) {
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

    delete_replacement_group = function () {
        $.post("/filtering/replacement_group/delete/" + $('#deleting_replacement_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_replacement_group_table();
            }
        });
    },

    load_replacement_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/filtering/replacement_group/list/", function (data) {
            $('#replacement_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_replacement_groups_message').hide();
                $('#replacement_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#replacement_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_replacement_group_btn_" + elem.id + "' href='#add_replacement_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a class='no_decoration' id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#add_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_replacement_group_" + elem.id + "' class='delete_replacement_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_replacement_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_replacement_group_btn_' + elem.id).click(function () {
                        edit_replacement_group(elem);
                    });

                    $('#delete_replacement_group_' + elem.id).click(function () {
                        $('#deleting_replacement_group_id').val(elem.id);
                    });

                    $('#link_channels_' + elem.id).click(function () {
                        manage_linked_channels(elem);
                    });
                });
            }else{
                $('#replacement_group_list_table').hide();
                $('#no_replacement_groups_message').show();
            }
        });
    },

    clear_add_replacement_group_form = function () {
        "use strict";

        $('#editing_replacement_group_id').val('');
        $('#add_replacement_group_name').val('');
        $('#replacements_box').hide();
        $('#save_replacement_group_btn').removeAttr("data-dismiss");
    },

    replacement_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_replacement_group = function () {
        "use strict";

        var 
            url,
            new_group = ($('#editing_replacement_group_id').val() == "")? true : false;

        if (new_group) {
            url = "/filtering/replacement_group/add/";
        }else{
            url = "/filtering/replacement_group/update/" + $('#editing_replacement_group_id').val();
        }

        $.post(url, {
            'replacement_group_name': $.trim($('#add_replacement_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_replacement_group_table();
                if(new_group){
                    edit_replacement_group(data.group_obj);
                }
            }else{
                if (data.result == "duplicate") {
                    alert("Ya existe un grupo con el nombre introducido");
                }
            }
        });

    },

    validate_add_replacement_group_form = function () {
        "use strict";

        if($.trim($('#add_replacement_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_filtering_li').addClass("active");
    
    clear_add_replacement_group_form();
    load_replacement_group_table();

    $('#save_replacement_group_btn').click(function () {
        if(validate_add_replacement_group_form()){
            submit_replacement_group();
        }else{
            return false;
        }
    });

    $('#add_replacement_group_btn').click(function () {
        $('#replacement_group_modal_title').text("Crear grupo de supresores");
        clear_add_replacement_group_form();
    });

    $('#add_replacement_btn').click(function () {
        submit_new_replacement();
    });

    $('#add_channels_modal').click(function () {
        /////
    });

    $('#save_channels_btn').click(function () {
        submit_channels();
    });

    $('#delete_replacement_group_confirmed').click(function () {
        delete_replacement_group();
    });

    $('#add_replacement_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_replacement();
        }
    });

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
    
});