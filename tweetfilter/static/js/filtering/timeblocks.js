
var

    load_timeblock_table = function () {
        "use strict";

        $.get("/filtering/timeblock/list/" + $('#current_channel').val(), function (data) {
            $('#timeblock_list_tbody').empty();

            if (data.length > 0) {
                $('#no_timeblocks_message').hide();
                $('#timeblock_list_table').show();

                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {

                    $('#timeblock_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.time + "</td>" +
                            "<td>" + elem.days + "</td>" +
                            "<td>" + elem.allows + "</td>" +
                            "<td><a id='delete_timeblock_" + elem.id +"' class='delete_filter' " +
                            "title='Haga click para eliminar filtro' href='#delete_timeblock_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#delete_timeblock_' + elem.id).click(function () {
                        $('#deleting_timeblock_id').val(elem.id);
                    });

                });
                $('#timeblock_list').show();
                $('#timeblock_list_div').slimscroll();
            }else{
                $('#timeblock_list').hide();
                $('#no_timeblocks_message').show();
            }
        });
    },

    timeblock_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_new_timeblock = function () {
        "use strict";

        $.post("/filtering/timeblock/add/", {
            'start': $('#start_timepicker').val(),
            'end': $('#end_timepicker').val(),
            'allow_mentions': $('#allow_mentions_check').is(':checked') ? 1 : 0,
            'allow_dm': $('#allow_dm_check').is(':checked') ? 1 : 0,
            'monday': $('#monday_check').is(':checked') ? 1 : 0,
            'tuesday': $('#tuesday_check').is(':checked') ? 1 : 0,
            'wednesday': $('#wednesday_check').is(':checked') ? 1 : 0,
            'thursday': $('#thursday_check').is(':checked') ? 1 : 0,
            'friday': $('#friday_check').is(':checked') ? 1 : 0,
            'saturday': $('#saturday_check').is(':checked') ? 1 : 0,
            'sunday': $('#sunday_check').is(':checked') ? 1 : 0,
            'timeblock_channel': $('#current_channel').val()
        }, function (data) {

            if(data.result === "ok") {
                load_timeblock_table();
                clear_add_timeblock_form();
            }else{
                timeblock_add_error(data.result);
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

    clear_add_timeblock_form = function () {
        "use strict";

        $('#start_timepicker').val('');
        $('#end_timepicker').val('');
        $('#allow_mentions_check').attr('checked', true);
        $('#allow_dm_check').attr('checked', true);
        check_all_days();
    },

    validate_add_timeblock_form = function () {
        "use strict";
        if($('#start_timepicker').val() == "" || $('#end_timepicker').val() == "") {
            alert("Debe ingresar los tiempos de inicio y fin");
            return false;
        }

        if($('#start_timepicker').val() >= $('#end_timepicker').val()) {
            alert("El tiempo de inicio debe ser menor al tiempo de fin");
            return false;
        }

        if(!$('#allow_mentions_check').is(":checked") && !$('#allow_dm_check').is(":checked")) {
            alert("Debe seleccionar al menos un tipo de mensaje (mentions o DM)");
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

    $('#timeblock_list').hide();
    $('#no_timeblocks_message').hide();
    $('#weekdays_select_div').show();

    clear_add_timeblock_form();
    load_timeblock_table();

    $('#start_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#end_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

      $('#delete_timeblock_confirmed').click(function () {
        $.post("/filtering/timeblock/delete/" + $('#deleting_timeblock_id').val(), function (data) {
            if(data.result === "ok") {
                load_timeblock_table();
            }
        });
    });

    $('#save_timeblock_btn').click(function () {
        if(validate_add_timeblock_form()){
            submit_new_timeblock();
        }else{
            return false;
        }
    });
});