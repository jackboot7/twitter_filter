var
    
    validate_add_hashtag_form = function () {
        "use strict";

        if($.trim($('#hashtag_text').val()) === ""){
            alert("Debe ingresar un texto para la publicación");
            return false;
        }

        if($.trim($('#hashtag_text').val()).length > 140){
            alert("Debe ingresar un texto menor a 140 caracteres");
            return false;
        }

        if($('#hashtag_timepicker').val() === ""){
            alert("Debe ingresar la hora de publicación");
            return false;
        }

        if (!($('#monday_check').is(':checked') ||
            $('#tuesday_check').is(':checked') ||
            $('#wednesday_check').is(':checked') ||
            $('#thursday_check').is(':checked') ||
            $('#friday_check').is(':checked') ||
            $('#saturday_check').is(':checked') ||
            $('#sunday_check').is(':checked'))){
            //Si no está chequeado ningún día
            alert("Debe seleccionar al menos un día de la semana");
            return false;
        }else{
            return true;
        }
    },

    show_add_hashtag_form = function () {
        $('#hashtag_table_div').hide();
        $('#add_hashtag_modal').show();
        $('#hashtag_group_modal_footer').hide();
    },

    hide_add_hashtag_form = function () {
        $('#add_hashtag_modal').hide();
        $('#hashtag_table_div').show();
        $('#hashtag_group_modal_footer').show();
    },

    edit_hashtag = function (hashtag) {
        "use strict";

        //alert(JSON.stringify(scheduled_post));
        $('#hashtag_modal_title').text("Editar hashtag");
        $('#editing_hashtag_id').val(hashtag.id);
        $('#add_hashtag_text').val(hashtag.text);
        $('#add_hashtag_qty').val(hashtag.quantity);

        $('#add_hashtag_start_timepicker').val(hashtag.start);
        $('#add_hashtag_end_timepicker').val(hashtag.end);
        $('#add_hashtag_monday_check').attr('checked', hashtag.monday);
        $('#add_hashtag_tuesday_check').attr('checked', hashtag.tuesday);
        $('#add_hashtag_wednesday_check').attr('checked', hashtag.wednesday);
        $('#add_hashtag_thursday_check').attr('checked', hashtag.thursday);
        $('#add_hashtag_friday_check').attr('checked', hashtag.friday);
        $('#add_hashtag_saturday_check').attr('checked', hashtag.saturday);
        $('#add_hashtag_sunday_check').attr('checked', hashtag.sunday);
    },

    submit_hashtag = function () {
        "use strict";

        var url;

        if ($('#editing_hashtag_id').val()) {
            url = "/scheduling/hashtag/update/" + $('#editing_hashtag_id').val();
        }else{
            url = "/scheduling/hashtag/add/";
        }

        $.post(url, {
            'text':$.trim($('#hashtag_text').val()),
            'time': $('#hashtag_timepicker').val(),
            'monday': $('#monday_check').is(':checked') ? 1 : 0,
            'tuesday': $('#tuesday_check').is(':checked') ? 1 : 0,
            'wednesday': $('#wednesday_check').is(':checked') ? 1 : 0,
            'thursday': $('#thursday_check').is(':checked') ? 1 : 0,
            'friday': $('#friday_check').is(':checked') ? 1 : 0,
            'saturday': $('#saturday_check').is(':checked') ? 1 : 0,
            'sunday': $('#sunday_check').is(':checked') ? 1 : 0,
            'group_id': $('#editing_hashtag_group_id').val()
        }, function (data) {
            if(data.result === "ok") {
                load_hashtag_table();
            }else{
                //scheduled_post_add_error(data.result);
                alert("hubo un error. Intente de nuevo");
            }

        });

    },

    clear_add_hashtag_form = function () {
        "use strict";

        hide_add_hashtag_form();

        $('#editing_hashtag_id').val('');
        $('#hashtag_timepicker').val('');
        $('#hashtag_text').val('');

        $('#monday_check').attr('checked', true);
        $('#tuesday_check').attr('checked', true);
        $('#wednesday_check').attr('checked', true);
        $('#thursday_check').attr('checked', true);
        $('#friday_check').attr('checked', true);
        $('#saturday_check').attr('checked', true);
        $('#sunday_check').attr('checked', true);

        count_characters();
    },

    submit_channels = function () {
        "use strict";
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/scheduling/hashtag_group/set_channels/" + $('#editing_hashtag_group_id').val(), {
            'channels': JSON.stringify(checked_channels)
        }, function (data) {
            /*
            if (data.result == "OK") {
                // alert todo bien
            }
            */
        });
    },

    delete_hashtag = function (hashtag_id) {
        "use strict";

        $.post("/scheduling/hashtag/delete/" + hashtag_id, function (data) {
            if(data.result === "ok") {
                load_hashtag_table();
            }
        });
    },

    load_hashtag_table = function () {
        "use strict";

        $.get("/scheduling/hashtag/list/" + $('#editing_hashtag_group_id').val(), function (data) {
            $('#hashtag_list_tbody').empty();

            if (data.length > 0) {
                var modal_body = $($('#add_hashtag_modal').html());

                $('#no_hashtags_message').hide();
                $('#hashtag_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#hashtag_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_hashtag_" + elem.id + "' href='#'>" + elem.text_excerpt + "</a></td>" +
                            "<td>" + elem.date_time + "</td>" +
                            "<td><a href='#' id='delete_hashtag_" + elem.id +"' class='delete_hashtag' " +
                            "title='Haga click para eliminar tweet programado'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#edit_hashtag_' + elem.id).click(function () {
                        edit_hashtag(elem);
                    });

                    $('#delete_hashtag_' + elem.id).click(function () {
                        delete_hashtag(elem.id);
                    });
                });

                $('#hashtag_list_div').slimscroll();
            }else{
                $('#hashtag_list_table').hide();
                $('#no_hashtags_message').show();
            }
        });
    },

    edit_hashtag_group = function (group) {
        "use strict";

        $('#hashtag_group_modal_title').text("Editar grupo de tweets programados");
        $('#editing_hashtag_group_id').val(group.id);
        $('#add_hashtag_group_name').val(group.name);
        $('#hashtags_box').show();
        $('#save_hashtag_group_btn').attr('data-dismiss', "modal");

        load_hashtag_table();
        $('#hashtag_table_div').show();
    },

    manage_linked_channels = function (group) {
        "use strict";

        $('#editing_hashtag_group_id').val(group.id);
        
        /*$.each(group.channels, function (index, value) {
            $("#link_channels_select").hashtag('[value="' + value + '"]').prop('selected', true);
        }); */
        
        $.get("/scheduling/hashtag_group/list_channels/" + group.id, {}, function (data) {
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

    delete_hashtag_group = function () {
        "use strict";

        $.post("/scheduling/hashtag_group/delete/" + $('#deleting_hashtag_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_hashtag_group_table();
            }
        });
    },

    load_hashtag_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/scheduling/hashtag_group/list/", function (data) {
            $('#hashtag_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_hashtag_groups_message').hide();
                $('#hashtag_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#hashtag_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_hashtag_group_btn_" + elem.id + "' href='#add_hashtag_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a class='no_decoration' id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#add_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_hashtag_group_" + elem.id + "' class='delete_hashtag_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_hashtag_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_hashtag_group_btn_' + elem.id).click(function () {
                        edit_hashtag_group(elem);
                    });

                    $('#delete_hashtag_group_' + elem.id).click(function () {
                        $('#deleting_hashtag_group_id').val(elem.id);
                    });

                    $('#link_channels_' + elem.id).click(function () {
                        manage_linked_channels(elem);
                    });
                });
            }else{
                $('#hashtag_group_list_table').hide();
                $('#no_hashtag_groups_message').show();
            }
        });
    },

    clear_add_hashtag_group_form = function () {
        "use strict";

        $('#editing_hashtag_group_id').val('');
        $('#add_hashtag_group_name').val('');
        $('#hashtags_box').hide();
        $('#save_hashtag_group_btn').removeAttr("data-dismiss");
    },

    hashtag_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_hashtag_group = function () {
        "use strict";

        var 
            url,
            new_group = ($('#editing_hashtag_group_id').val() == "")? true : false;

        if (new_group) {
            url = "/scheduling/hashtag_group/add/";
        }else{
            url = "/scheduling/hashtag_group/update/" + $('#editing_hashtag_group_id').val();
        }

        $.post(url, {
            'hashtag_group_name': $.trim($('#add_hashtag_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_hashtag_group_table();
                if(new_group){
                    edit_hashtag_group(data.group_obj);
                }
            }else{
                if (data.result == "duplicate") {
                    alert("Ya existe un grupo con el nombre introducido");
                }
            }
        });

    },

    validate_add_hashtag_group_form = function () {
        "use strict";

        if($.trim($('#add_hashtag_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
    },

    count_characters = function () {
        "use strict";

        var count = 140 - parseInt($('#hashtag_text').val().length, 10);
        $('#tweet_char_count').text(count);
        if(count > 20){
            $('#tweet_char_count').css({'color': '#999999'});
        }else if(count <= 10){
            $('#tweet_char_count').css({'color': '#D40D12'});
        }else{
            $('#tweet_char_count').css({'color': '#5C0002'});
        }
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_hashtags_li').addClass("active");
    
    clear_add_hashtag_group_form();
    clear_add_hashtag_form();
    load_hashtag_group_table();

    $('#hashtag_table_div').hide();

    $('#send_now_confirmed').click(function () {
        $.post("/scheduling/send/" + $('#sending_now_tweet_id').val(),
            function (data) {
                if(data.result === "ok") {
                    $('#alert_success_body').text("El tweet fue enviado con éxito");
                    $('#alert_success').show();
                }else{
                    $('#alert_warning_body').text(data.error_msg);
                    $('#alert_warning').show();
                }
            });
    });

    $('#save_hashtag_group_btn').click(function () {
        if(validate_add_hashtag_group_form()){
            submit_hashtag_group();
        }else{
            return false;
        }
    });

    $('#add_hashtag_group_btn').click(function () {
        $('#hashtag_group_modal_title').text("Crear grupo de tweets programados");
        clear_add_hashtag_group_form();
    });


    /*$('#add_channels_modal').click(function () {
        /////
    });*/

    $('#save_channels_btn').click(function () {
        submit_channels();
    });

    $('#delete_hashtag_group_confirmed').click(function () {
        delete_hashtag_group();
    });

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
    
    $('#add_hashtag_btn').click(function () {
        $('#hashtag_modal_title').text("Agregar tweet programado");
        show_add_hashtag_form();
    });

    $('#close_hashtag_form').click(function () {
        hide_add_hashtag_form();
    });

    $('#save_hashtag_btn').click(function () {
        if(validate_add_hashtag_form()){
            submit_hashtag();
            clear_add_hashtag_form();
        }else{
            return false;
        }
    });

    $('#hashtag_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#hashtag_text').bind("keyup change input", function () {
        count_characters();
    });    

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
});