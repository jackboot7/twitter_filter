var

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

    update_hashtags_status = function () {
        "use strict";

        $.get("/hashtags/check_status/" + $('#current_channel').val(), function (data) {
            var
                btn = $('#switch_hashtags_btn'),
                label = $('#switch_hashtags_label');

            if(data.result === "enabled"){
                btn.attr('title', "Haga click para desactivar");
                label.text("Activo");
                label.removeClass('label-important').addClass('label-success');
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
            }
        });
    },

    load_hashtag_table = function () {
        "use strict";

        $.get("/hashtags/list/" + $('#current_channel').val(), function (data) {
            $('#hashtag_list_tbody').empty();

            if (data.length > 0) {
                $('#no_hashtags_message').hide();
                $('#hashtag_list_table').show();

                $.each(data, function (idx, elem) {

                    $('#hashtag_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_hashtag_" + elem.id + "' href='#add_hashtag_modal' data-toggle='modal'>#" + elem.text + "</a></td>" +
                            "<td>" + elem.quantity + "</td>" +
                            //"<td>"+ "</td>" +   // horario
                            "<td><a id='delete_hashtag_" + elem.id +"' class='delete_hashtag' " +
                            "title='Haga click para eliminar el hashtag' href='#delete_hashtag_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_hashtag_' + elem.id).click(function () {
                        edit_hashtag(elem);
                    });

                    $('#delete_hashtag_' + elem.id).click(function () {
                        $('#deleting_hashtag_id').val(elem.id);
                    });
                });
                $('#hashtag_list_table').show();
            }else{
                $('#hashtag_list_table').hide();
                $('#no_hashtags_message').show();
            }
        });
    },

    hashtag_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_hashtag = function () {
        "use strict";

        var url;

        if ($('#editing_hashtag_id').val() === "") {
            url = "/hashtags/add/";
        }else{
            url = "/hashtags/update/" + $('#editing_hashtag_id').val();
        }

        $.post(url, {
            'text': $.trim($('#add_hashtag_text').val()),
            'qty': $.trim($('#add_hashtag_qty').val()),
            'channel': $('#current_channel').val(),
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

    validate_add_hashtag_form = function () {
        "use strict";

        if($.trim($('#add_hashtag_text').val()) === ""){
            alert("Debe ingresar un texto para el hashtag");
            return false;
        }

        if((/^[a-zA-Z_][a-zA-Z0-9_]{1,138}$/g).test($.trim($('#add_hashtag_text').val()))){
            alert("El texto no debe contener '#' ni otros caracteres especiales");
            return false;
        }

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
    };


$(document).ready(function () {
    "use strict";

    $('#hashtag_list_table').hide();
    $('#no_hashtags_message').hide();

    update_hashtags_status();
    clear_add_hashtag_form();
    load_hashtag_table();

    $('#switch_hashtags_btn').click(function () {
        $.post("/hashtags/switch_status/" + $('#current_channel').val(), function (data) {
            update_hashtags_status();
        });
    });


    $('#delete_hashtag_confirmed').click(function () {
        $.post("/hashtags/delete/" + $('#deleting_hashtag_id').val(),
            function (data) {
            if(data.result === "ok") {
                load_hashtag_table();
            }
        });
    });

    $('#save_hashtag_btn').click(function () {
        if(validate_add_hashtag_form()){
            submit_hashtag();
        }else{
            return false;
        }
    });

    $('#add_hashtag_btn').click(function () {
        $('#hashtag_modal_title').text("Añadir hashtag");
        clear_add_hashtag_form();
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