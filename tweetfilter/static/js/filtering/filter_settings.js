var
    /*
    filter_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },*/
    submit_channels = function () {
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/filtering/filter_group/set_channels/" + $('#editing_filter_group_id').val(), {
            'channels': JSON.stringify(checked_channels)
        }, function (data) {
            /*
            if (data.result == "OK") {
                // alert todo bien
            }
            */
        });
    },

    submit_new_filter = function () {
        "use strict";

        var filter_text = $.trim($('#add_filter_text').val());
        if(filter_text.length > 0) {
            $.post("/filtering/filter/add/", {
                'filter_text': filter_text,
                'group_id': $('#editing_filter_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_filter_text').val("");
                    load_filter_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //filter_add_error(data.result)
                }
            });
        }
    },

    delete_filter = function (filter_id) {
        $.post("/filtering/filter/delete/" + filter_id, function (data) {
            if(data.result === "ok") {
                load_filter_table();
            }
        });
    },

    load_filter_table = function () {
        "use strict";

        $.get("/filtering/filter/list/" + $('#editing_filter_group_id').val(), function (data) {
            $('#filter_list_tbody').empty();

            if (data.length > 0) {
                $('#no_filters_message').hide();
                $('#filter_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#filter_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td><a href='#' id='delete_filter_" + elem.id +"' class='delete_filter' " +
                            "title='Haga click para eliminar retenedor'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#delete_filter_' + elem.id).click(function () {
                        delete_filter(elem.id);
                    });
                });

                $('#filter_list_div').slimscroll();
            }else{
                $('#filter_list_table').hide();
                $('#no_filters_message').show();
            }
        });
    },

    edit_filter_group = function (group) {
        "use strict";

        $('#filter_group_modal_title').text("Editar grupo de retenedores");
        $('#editing_filter_group_id').val(group.id);
        $('#add_filter_group_name').val(group.name);
        $('#filters_box').show();
        $('#save_filter_group_btn').attr('data-dismiss', "modal");

        load_filter_table();
        // mostrar lista de filters
    },

    manage_linked_channels = function (group) {
        $('#editing_filter_group_id').val(group.id);
        
        /*$.each(group.channels, function (index, value) {
            $("#link_channels_select").filter('[value="' + value + '"]').prop('selected', true);
        }); */
        
        $.get("/filtering/filter_group/list_channels/" + group.id, {}, function (data) {
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

    delete_filter_group = function () {
        $.post("/filtering/filter_group/delete/" + $('#deleting_filter_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_filter_group_table();
            }
        });
    },

    load_filter_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/filtering/filter_group/list/", function (data) {
            $('#filter_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_filter_groups_message').hide();
                $('#filter_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#filter_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_filter_group_btn_" + elem.id + "' href='#add_filter_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a class='no_decoration' id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#add_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_filter_group_" + elem.id + "' class='delete_filter_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_filter_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_filter_group_btn_' + elem.id).click(function () {
                        edit_filter_group(elem);
                    });

                    $('#delete_filter_group_' + elem.id).click(function () {
                        $('#deleting_filter_group_id').val(elem.id);
                    });

                    $('#link_channels_' + elem.id).click(function () {
                        manage_linked_channels(elem);
                    });
                });
            }else{
                $('#filter_group_list_table').hide();
                $('#no_filter_groups_message').show();
            }
        });
    },

    clear_add_filter_group_form = function () {
        "use strict";

        $('#editing_filter_group_id').val('');
        $('#add_filter_group_name').val('');
        $('#filters_box').hide();
        $('#save_filter_group_btn').removeAttr("data-dismiss");
    },

    filter_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_filter_group = function () {
        "use strict";

        var 
            url,
            new_group = ($('#editing_filter_group_id').val() == "")? true : false;

        if (new_group) {
            url = "/filtering/filter_group/add/";
        }else{
            url = "/filtering/filter_group/update/" + $('#editing_filter_group_id').val();
        }

        $.post(url, {
            'filter_group_name': $.trim($('#add_filter_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_filter_group_table();
                if(new_group){
                    edit_filter_group(data.group_obj);
                }
            }else{
                if (data.result == "duplicate") {
                    alert("Ya existe un grupo con el nombre introducido");
                }
            }
        });

    },

    validate_add_filter_group_form = function () {
        "use strict";

        if($.trim($('#add_filter_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_filtering_li').addClass("active");
    
    clear_add_filter_group_form();
    load_filter_group_table();

    $('#save_filter_group_btn').click(function () {
        if(validate_add_filter_group_form()){
            submit_filter_group();
        }else{
            return false;
        }
    });

    $('#add_filter_group_btn').click(function () {
        $('#filter_group_modal_title').text("Crear grupo de retenedores");
        clear_add_filter_group_form();
    });

    $('#add_filter_btn').click(function () {
        submit_new_filter();
    });

    $('#add_channels_modal').click(function () {
        /////
    });

    $('#save_channels_btn').click(function () {
        submit_channels();
    });

    $('#delete_filter_group_confirmed').click(function () {
        delete_filter_group();
    });

    $('#add_filter_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_filter();
        }
    });

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
});