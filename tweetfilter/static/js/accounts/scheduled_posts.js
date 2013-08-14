
var

    load_scheduled_post_table = function () {
        "use strict";

        $.get("/scheduled_posts/list/" + $('#current_channel').val(), function (data) {
            $('#scheduled_post_list_tbody').empty();

            if (data.length > 0) {
                $('#no_scheduled_posts_message').hide();
                $('#scheduled_post_list_table').show();

                $.each(data, function (idx, elem) {

                    $('#scheduled_post_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + elem.date_time + "</td>" +
                            "<td><a id='delete_scheduled_post_" + elem.id +"' class='delete_scheduled_post' " +
                            "title='Haga click para eliminar el bloque' href='#delete_scheduled_post_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

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

    submit_new_scheduled_post = function () {
        "use strict";

        $.post("/scheduled_posts/add/", {
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

    clear_add_scheduled_post_form = function () {
        "use strict";

        $('#scheduled_post_timepicker').val('');
        check_all_days();
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

    clear_add_scheduled_post_form();
    load_scheduled_post_table();

    $('#scheduled_post_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#delete_scheduled_post_confirmed').click(function () {
        $.post("/scheduled_posts/delete/" + $('#deleting_scheduled_post_id').val(),
            function (data) {
            if(data.result === "ok") {
                load_scheduled_post_table();
            }
        });
    });

    $('#save_scheduled_post_btn').click(function () {
        if(validate_add_scheduled_post_form()){
            submit_new_scheduled_post();
        }else{
            return false;
        }
    });
});