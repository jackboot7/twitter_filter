
var

    edit_scheduled_post = function (scheduled_post) {
        "use strict";

        //alert(JSON.stringify(scheduled_post));
        $('#scheduled_post_modal_title').text("Editar tweet programado");
        $('#editing_scheduled_post_id').val(scheduled_post.id);

        $('#scheduled_post_text').val(scheduled_post.text);
        $('#scheduled_post_timepicker').val(scheduled_post.time);
        $('#monday_check').attr('checked', scheduled_post.monday);
        $('#tuesday_check').attr('checked', scheduled_post.tuesday);
        $('#wednesday_check').attr('checked', scheduled_post.wednesday);
        $('#thursday_check').attr('checked', scheduled_post.thursday);
        $('#friday_check').attr('checked', scheduled_post.friday);
        $('#saturday_check').attr('checked', scheduled_post.saturday);
        $('#sunday_check').attr('checked', scheduled_post.sunday);

        count_characters();
    },

    update_scheduling_status = function () {
        "use strict";

        $.get("/scheduling/check_status/" + $('#current_channel').val(), function (data) {
            var
                btn = $('#switch_scheduling_btn'),
                label = $('#switch_scheduling_label');

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

    load_scheduled_post_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();
        $.get("/scheduling/list/" + $('#current_channel').val(), function (data) {
            $('#scheduled_post_list_tbody').empty();

            if (data.length > 0) {
                $('#no_scheduled_posts_message').hide();
                $('#scheduled_post_list_table').show();

                $.each(data, function (idx, elem) {

                    $('#scheduled_post_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_scheduled_post_" + elem.id + "' href='#add_scheduled_post_modal' data-toggle='modal'>" + elem.text_excerpt + "</a></td>" +
                            "<td>" + elem.date_time + "</td>" +
                            "<td><a id='send_now_" + elem.id + "' class='send_tweet_now' " +
                            "title='Haga click para enviar el mensaje ahora' href='#send_now_confirm_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/send_now.png'></a></td>" +
                            "<td><a id='delete_scheduled_post_" + elem.id +"' class='delete_scheduled_post' " +
                            "title='Haga click para eliminar el bloque' href='#delete_scheduled_post_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_scheduled_post_' + elem.id).click(function () {
                        edit_scheduled_post(elem);
                    });

                    $('#send_now_' + elem.id).click(function (){
                        $('#sending_now_tweet_id').val(elem.id);
                        $('#sending_now_tweet_text').text(elem.text);
                    });

                    $('#delete_scheduled_post_' + elem.id).click(function () {
                        $('#deleting_scheduled_post_id').val(elem.id);
                    });
                });
                $('#scheduled_post_list').show();
            }else{
                $('#scheduled_post_list').hide();
                $('#no_scheduled_posts_message').show();
            }
        });
    },

    scheduled_post_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_scheduled_post = function () {
        "use strict";

        var url;

        if ($('#editing_scheduled_post_id').val() === "") {
            url = "/scheduling/add/";
        }else{
            url = "/scheduling/update/" + $('#editing_scheduled_post_id').val();
        }

        $.post(url, {
            'text':$.trim($('#scheduled_post_text').val()),
            'time': $('#scheduled_post_timepicker').val(),
            'monday': $('#monday_check').is(':checked') ? 1 : 0,
            'tuesday': $('#tuesday_check').is(':checked') ? 1 : 0,
            'wednesday': $('#wednesday_check').is(':checked') ? 1 : 0,
            'thursday': $('#thursday_check').is(':checked') ? 1 : 0,
            'friday': $('#friday_check').is(':checked') ? 1 : 0,
            'saturday': $('#saturday_check').is(':checked') ? 1 : 0,
            'sunday': $('#sunday_check').is(':checked') ? 1 : 0,
            'channel': $('#current_channel').val()
        }, function (data) {

            if(data.result === "ok") {
                load_scheduled_post_table();
                clear_add_scheduled_post_form();
            }else{
                scheduled_post_add_error(data.result);
            }
        });

    },

    check_all_days = function () {
        "use strict";

        $('#monday_check').attr('checked', true);
        $('#tuesday_check').attr('checked', true);
        $('#wednesday_check').attr('checked', true);
        $('#thursday_check').attr('checked', true);
        $('#friday_check').attr('checked', true);
        $('#saturday_check').attr('checked', true);
        $('#sunday_check').attr('checked', true);
    },

    count_characters = function () {
        "use strict";

        var count = 140 - parseInt($('#scheduled_post_text').val().length, 10);
        $('#tweet_char_count').text(count);
        if(count > 20){
            $('#tweet_char_count').css({'color': '#999999'});
        }else if(count <= 10){
            $('#tweet_char_count').css({'color': '#D40D12'});
        }else{
            $('#tweet_char_count').css({'color': '#5C0002'});
        }
    },

    clear_add_scheduled_post_form = function () {
        "use strict";

        $('#editing_scheduled_post_id').val('');
        $('#scheduled_post_timepicker').val('');
        $('#scheduled_post_text').val('');
        check_all_days();
        count_characters();
    },

    validate_add_scheduled_post_form = function () {
        "use strict";

        if($.trim($('#scheduled_post_text').val()) === ""){
            alert("Debe ingresar un texto para la publicación");
            return false;
        }

        if($.trim($('#scheduled_post_text').val()).length > 140){
            alert("Debe ingresar un texto menor a 140 caracteres");
            return false;
        }

        if($('#scheduled_post_timepicker').val() === ""){
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
    };


$(document).ready(function () {
    "use strict";

    $('#scheduled_post_list').hide();
    $('#no_scheduled_posts_message').hide();
    $('#weekdays_select_div').show();

    update_scheduling_status();
    clear_add_scheduled_post_form();
    load_scheduled_post_table();

    $('#switch_scheduling_btn').click(function () {
        $.post("/scheduling/switch_status/" + $('#current_channel').val(), function (data) {
            update_scheduling_status();
        });
    });

    $('#scheduled_post_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#scheduled_post_text').bind("keyup change input", function () {
        count_characters();
    });

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

    $('#delete_scheduled_post_confirmed').click(function () {
        $.post("/scheduling/delete/" + $('#deleting_scheduled_post_id').val(),
            function (data) {
            if(data.result === "ok") {
                load_scheduled_post_table();
            }
        });
    });

    $('#save_scheduled_post_btn').click(function () {
        if(validate_add_scheduled_post_form()){
            submit_scheduled_post();
        }else{
            return false;
        }
    });

    $('#add_scheduled_post_btn').click(function () {
        $('#scheduled_post_modal_title').text("Añadir tweet programado");
        clear_add_scheduled_post_form();
    });
});