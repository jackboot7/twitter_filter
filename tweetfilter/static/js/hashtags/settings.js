var
    
    reset_hashtag = function (hashtag_id) {
        $.post("/hashtags/hashtag/reset/" + hashtag_id, function (data) {
            if(data.result === "ok") {
                $('#hashtag_count_span_' + hashtag_id).text('0');
            }
        });
    },

    validate_add_hashtag_form = function () {
        "use strict";

        if($.trim($('#add_hashtag_text').val()) === ""){
            alert("Debe ingresar un texto para el sufijo");
            return false;
        }

        /*
        if(!(/^[a-zA-Z0-9_áéíóúÁÉÍÓÚñÑ]{1,139}$/g).test($.trim($('#add_hashtag_text').val()))){
            alert("El texto no debe contener '#' ni otros caracteres especiales");
            return false;
        }else if(!(/[a-zA-Z]/g).test($.trim($('#add_hashtag_text').val()))){
            alert("El texto debe contener al menos una letra");
            return false;
        }
        */

        if(!/^[0-9]+$/.test($.trim($('#add_hashtag_qty').val()))){
            alert("Debe ingresar un número entero como cantidad");
            return false;
        }

        if($('#add_hashtag_start_timepicker').val() === ""){
            alert("Debe ingresar una hora de inicio");
            return false;
        }

        if($('#add_hashtag_end_timepicker').val() === ""){
            alert("Debe ingresar una hora de finalización");
            return false;
        }

        if($('#start_timepicker').val() >= $('#end_timepicker').val()) {
            alert("El tiempo de inicio debe ser menor al tiempo de fin");
            return false;
        }

        if (!($('#add_hashtag_monday_check').is(':checked') ||
            $('#add_hashtag_tuesday_check').is(':checked') ||
            $('#add_hashtag_wednesday_check').is(':checked') ||
            $('#add_hashtag_thursday_check').is(':checked') ||
            $('#add_hashtag_friday_check').is(':checked') ||
            $('#add_hashtag_saturday_check').is(':checked') ||
            $('#add_hashtag_sunday_check').is(':checked'))){
            //Si no está chequeado ningún día
            alert("Debe seleccionar al menos un día de la semana");
            return false;
        }

        return true;
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

        show_add_hashtag_form();

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

        if ($('#editing_hashtag_id').val() === "") {
            url = "/hashtags/hashtag/add/";
        }else{
            url = "/hashtags/hashtag/update/" + $('#editing_hashtag_id').val();
        }

        $.post(url, {
            'text': $.trim($('#add_hashtag_text').val()),
            'qty': $.trim($('#add_hashtag_qty').val()),
            'group_id': $('#editing_hashtag_group_id').val(),
            'start': $('#add_hashtag_start_timepicker').val(),
            'end': $('#add_hashtag_end_timepicker').val(),
            'monday': $('#add_hashtag_monday_check').is(':checked') ? 1 : 0,
            'tuesday': $('#add_hashtag_tuesday_check').is(':checked') ? 1 : 0,
            'wednesday': $('#add_hashtag_wednesday_check').is(':checked') ? 1 : 0,
            'thursday': $('#add_hashtag_thursday_check').is(':checked') ? 1 : 0,
            'friday': $('#add_hashtag_friday_check').is(':checked') ? 1 : 0,
            'saturday': $('#add_hashtag_saturday_check').is(':checked') ? 1 : 0,
            'sunday': $('#add_hashtag_sunday_check').is(':checked') ? 1 : 0
            // otros campos
        }, function (data) {

            if(data.result === "ok") {
                load_hashtag_table();
                clear_add_hashtag_form();
            }else{
                hashtag_add_error(data.result);
            }
        });

    },

    clear_add_hashtag_form = function () {
        "use strict";

        hide_add_hashtag_form();

        $('#editing_hashtag_id').val('');
        $('#add_hashtag_text').val('');
        $('#add_hashtag_qty').val('');

        $('#add_hashtag_start_timepicker').val('');
        $('#add_hashtag_end_timepicker').val('');
        $('#add_hashtag_monday_check').attr('checked', true);
        $('#add_hashtag_tuesday_check').attr('checked', true);
        $('#add_hashtag_wednesday_check').attr('checked', true);
        $('#add_hashtag_thursday_check').attr('checked', true);
        $('#add_hashtag_friday_check').attr('checked', true);
        $('#add_hashtag_saturday_check').attr('checked', true);
        $('#add_hashtag_sunday_check').attr('checked', true);
    },

    submit_channels = function () {
        "use strict";
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/hashtags/hashtag_group/set_channels/" + $('#editing_hashtag_group_id').val(), {
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

        $.post("/hashtags/hashtag/delete/" + hashtag_id, function (data) {
            if(data.result === "ok") {
                load_hashtag_table();
            }
        });
    },

    load_hashtag_table = function () {
        "use strict";
        var static_url = $('#static_url_path').val();

        $.get("/hashtags/hashtag/list/" + $('#editing_hashtag_group_id').val(), function (data) {
            $('#hashtag_list_tbody').empty();

            if (data.length > 0) {
                $('#no_hashtags_message').hide();
                $('#hashtag_list_table').show();

                $.each(data, function (idx, elem) {
                    var text = (elem.text.length > 16)? elem.text.substr(0,16) + "..." : elem.text;
                    $('#hashtag_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_hashtag_" + elem.id + "' href='#add_hashtag_modal' data-toggle='modal'>" + text + "</a></td>" +
                            "<td>" + elem.quantity + "</td>" +
                            "<td><span id='hashtag_count_span_" + elem.id + "'>"+ elem.count + "</span></td>" +
                            "<td><a id='reset_hashtag_" + elem.id + "' class='reset_hashtag' " +
                            "title='Haga click para reiniciar el contador' href='#reset_hashtag_confirm_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/refresh_20.png'></a></td>" +
                            "<td><a id='delete_hashtag_" + elem.id + "' class='delete_hashtag' " +
                            "title='Haga click para eliminar el hashtag' href='#'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_hashtag_' + elem.id).click(function () {
                        edit_hashtag(elem);
                    });

                    $('#delete_hashtag_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea eliminar el sufijo seleccionado?")) {
                            delete_hashtag(elem.id);
                        }
                    });

                    $('#reset_hashtag_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea reiniciar el contador de ocurrencias del sufijo seleccionado?")) {
                            reset_hashtag(elem.id);
                        }
                    });
                });
                $('#hashtag_list_table').show();
            }else{
                $('#hashtag_list_table').hide();
                $('#no_hashtags_message').show();
            }
        });
    },

    edit_hashtag_group = function (group) {
        "use strict";

        $('#hashtag_group_modal_title').text("Editar grupo de sufijos");
        $('#editing_hashtag_group_id').val(group.id);
        $('#add_hashtag_group_name').val(group.name);
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
        
        $.get("/hashtags/hashtag_group/list_channels/" + group.id, {}, function (data) {
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

        $.post("/hashtags/hashtag_group/delete/" + $('#deleting_hashtag_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_hashtag_group_table();
            }
        });
    },

    load_hashtag_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/hashtags/hashtag_group/list/", function (data) {
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

        $('#hashtag_table_div').hide();
        $('#editing_hashtag_group_id').val('');
        $('#add_hashtag_group_name').val('');
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
            url = "/hashtags/hashtag_group/add/";
        }else{
            url = "/hashtags/hashtag_group/update/" + $('#editing_hashtag_group_id').val();
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
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_hashtags_li').addClass("active");
    
    clear_add_hashtag_group_form();
    clear_add_hashtag_form();
    load_hashtag_group_table();

    $('#hashtag_table_div').hide();
    $('#add_hashtag_modal').hide();

    $('#send_now_confirmed').click(function () {
        $.post("/hashtags/send/" + $('#sending_now_tweet_id').val(),
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
        $('#hashtag_group_modal_title').text("Crear grupo de sufijos programados");
        clear_add_hashtag_group_form();
    });

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
        $('#hashtag_modal_title').text("Agregar sufijo");
        clear_add_hashtag_form();
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

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });

    $('#add_hashtag_start_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#add_hashtag_end_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });
});