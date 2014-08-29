var

    reset_hashtag = function (hashtag_id) {
        $.post("/hashtags/hashtag/reset/" + hashtag_id, function (data) {
            if(data.result === "ok") {
                $('#hashtag_count_span_' + hashtag_id).text('0');
            }
        });
    },

    send_hashtag = function (tweet_id) {
        $.post("/hashtags/hashtag/send/" + tweet_id,
            function (data) {
                if(data.result === "ok") {
                    alert("El tweet fue enviado con éxito");
                }else{
                    alert(data.error_msg);
                }
        });
    },

    delete_hashtag = function (hashtag_id) {
        "use strict";

        $.post("/hashtags/hashtag/delete/" + hashtag_id, function (data) {
            if(data.result === "ok") {
                load_hashtag_table(true);
            }
        });
    },

    validate_add_hashtag_form = function () {
        "use strict";

        if($.trim($('#add_hashtag_text').val()) === ""){
            alert("Debe ingresar un texto para el sufijo");
            return false;
        }

        if(!/^[0-9]+$/.test($.trim($('#add_hashtag_qty').val()))){
            alert("Debe ingresar un número entero como límite");
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

        if($('#add_hashtag_start_timepicker').val() >= $('#add_hashtag_end_timepicker').val()) {
            alert("La hora de inicio debe ser menor a la hora de fin");
            return false;
        }

        if ($('#add_hashtag_start_datepicker').val() != "" && $('#add_hashtag_end_datepicker').val() != "") {
            if ($('#add_hashtag_start_datepicker').val() > $('#add_hashtag_end_datepicker').val()) {
                alert("La fecha de inicio debe ser menor o igual a la fecha de fin");
                return false;
            }
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

    disable_hashtag_form = function () {
        "use strict";

        // disable fields?
        $("#disable_hashtag_btn").hide();
        $("#enable_hashtag_btn").show();
    },

    enable_hashtag_form = function () {
        "use strict";

        // enable fields?
        $("#enable_hashtag_btn").hide();
        $("#disable_hashtag_btn").show();
    },

    enable_hashtag = function () {
        "use strict";

        $.post("/hashtags/hashtag/enable/" + $("#editing_hashtag_id").val(), function (data) {
            if(data.result === "ok") {
                enable_hashtag_form();
            }
        });
    },

    disable_hashtag = function () {
        "use strict";

        $.post("/hashtags/hashtag/disable/" + $("#editing_hashtag_id").val(), function (data) {
            if(data.result === "ok") {
                disable_hashtag_form();
            }
        });
    },

    edit_hashtag = function (hashtag) {
        "use strict";

        var
            start_date_arr,
            end_date_arr,
            start_date = "",
            end_date = "";

        if (hashtag.start_date) {
            start_date_arr = hashtag.start_date.split("-");
            start_date = start_date_arr[2] + "/" + start_date_arr[1] + "/" + start_date_arr[0];
        }

        if (hashtag.end_date) {
            end_date_arr = hashtag.end_date.split("-");
            end_date = end_date_arr[2] + "/" + end_date_arr[1] + "/" + end_date_arr[0];
        }

        show_add_hashtag_form();

        $('#hashtag_modal_title').text("Editar hashtag");
        $('#editing_hashtag_id').val(hashtag.id);
        $('#add_hashtag_text').val(hashtag.text);
        $('#add_hashtag_qty').val(hashtag.limit);

        $('#add_hashtag_start_timepicker').val(hashtag.start);
        $('#add_hashtag_end_timepicker').val(hashtag.end);
        $('#add_hashtag_start_datepicker').val(start_date);
        $('#add_hashtag_end_datepicker').val(end_date);
        
        $('#add_hashtag_monday_check').attr('checked', hashtag.monday);
        $('#add_hashtag_tuesday_check').attr('checked', hashtag.tuesday);
        $('#add_hashtag_wednesday_check').attr('checked', hashtag.wednesday);
        $('#add_hashtag_thursday_check').attr('checked', hashtag.thursday);
        $('#add_hashtag_friday_check').attr('checked', hashtag.friday);
        $('#add_hashtag_saturday_check').attr('checked', hashtag.saturday);
        $('#add_hashtag_sunday_check').attr('checked', hashtag.sunday);

        if (hashtag.status == 1) {   // scheduled tweet is enabled
            enable_hashtag_form();
        } else {
            disable_hashtag_form();
        }

        $('#hashtag_status_row').show();
    },

    manage_linked_hashtag_groups = function () {
        $.get("/hashtags/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "Hashtag"
        }, function (data) {
            $("#hashtag_groups_select").multiselect("uncheckAll");        
            $("#hashtag_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });

            $("#hashtag_groups_select").multiselect("refresh");
        });
    },

    link_hashtag_groups = function () {
        var checked_groups = $("#hashtag_groups_select").val();

        $.post("/hashtags/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "Hashtag"
        }, function (data) {
            load_hashtag_group_table();
        });
    },

    unlink_hashtag_group = function(group_id) {
        $.post("/hashtags/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_hashtag_group_table();
        });
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
                $("#hashtags_status").val("active");
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
                $("#hashtags_status").val("inactive");
            }
        });
    },

    view_hashtag_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_hashtag_group_name').html(group_name);
        $('#viewing_hashtag_group_id').val(group_id);
                
        if (exclusive) {
            $('#delete_hashtag_header').show();
            $('#add_hashtag_btn').show();
        } else {
            $('#delete_hashtag_header').hide();
            $('#add_hashtag_btn').hide();
        }
        
        load_hashtag_table(exclusive);
    },

    load_hashtag_group_table = function () {
        "use strict";
        
        $.get("/hashtags/hashtag_group/channel/"+$('#current_channel').val(), function (data) {
            $('#hashtag_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_hashtag_header').hide();
            } else {
                $('#unlink_hashtag_header').show();
            }

            $('#hashtag_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";

                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_hashtag_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#hashtag_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_hashtag_group_modal' data-toggle='modal' id='view_hashtag_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_hashtag_group_" + elem.id).click(function () {
                    view_hashtag_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
                    $('#delete_hashtag_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_hashtag_group(elem.id);
                        }
                    });
                }
            });

            $('#hashtag_group_list_div').slimscroll();
        });
    },

    load_hashtag_table = function (exclusive) {
        "use strict";

        var 
            delete_btn = "",
            edit_link = "",
            reset_btn = "",
            static_url = $('#static_url_path').val();

        $.get("/hashtags/hashtag/list/" + $('#viewing_hashtag_group_id').val(), function (data) {
            $('#hashtag_list_tbody').empty();

            if (data.length > 0) {
                $('#no_hashtags_message').hide();
                $('#hashtag_list_table').show();

                $.each(data, function (idx, elem) {
                    var text = (elem.text.length > 16)? elem.text.substr(0,16) + "..." : elem.text;
 
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_hashtag_" + elem.id +"' class='delete_hashtag' " +
                            "title='Haga click para eliminar el sufijo' href='#delete_hashtag_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                        edit_link = "<a id='edit_hashtag_" + elem.id + "' href='#' data-toggle='modal'>" + text + "</a>";
                        reset_btn = 
                            "<td><a id='reset_hashtag_" + elem.id + "' class='reset_hashtag' " +
                            "title='Haga click para reiniciar el contador' href='#reset_hashtag_confirm_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/refresh_20.png'></a></td>"
                    } else {
                        delete_btn = "";
                        edit_link = text;
                        reset_btn = "";
                    }

                    $('#hashtag_list_tbody').append(
                        "<tr>" +
                            "<td>" + edit_link + "</td>" +
                            "<td>" + elem.limit + "</td>" +
                            "<td><span id='hashtag_count_span_" + elem.id + "'>"+ elem.count + "</span></td>" +
                            reset_btn +
                            "<td>" + delete_btn + "</td>" +
                            "</tr>"
                    );

                    if (exclusive) {
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
                    }
                });

                $('#hashtag_list_div').show();
            }else{
                $('#hashtag_list_div').hide();
                $('#no_hashtags_message').show();
            }
        });
    },

    /*
    hashtag_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },
    */

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
            'group_id': $('#viewing_hashtag_group_id').val(),
            'start': $('#add_hashtag_start_timepicker').val(),
            'end': $('#add_hashtag_end_timepicker').val(),
            'start_date': $('#add_hashtag_start_datepicker').val(),
            'end_date': $('#add_hashtag_end_datepicker').val(),
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
                load_hashtag_table(true);
                clear_add_hashtag_form();
            }else{
                alert(data.result);
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

    clear_add_hashtag_form = function () {
        "use strict";

        hide_add_hashtag_form();

        $('#editing_hashtag_id').val('');
        $('#add_hashtag_text').val('');
        $('#add_hashtag_qty').val('');

        $('#add_hashtag_start_timepicker').val('');
        $('#add_hashtag_end_timepicker').val('');
        $('#add_hashtag_start_datepicker').val('');
        $('#add_hashtag_end_datepicker').val('');
        $('#add_hashtag_monday_check').attr('checked', true);
        $('#add_hashtag_tuesday_check').attr('checked', true);
        $('#add_hashtag_wednesday_check').attr('checked', true);
        $('#add_hashtag_thursday_check').attr('checked', true);
        $('#add_hashtag_friday_check').attr('checked', true);
        $('#add_hashtag_saturday_check').attr('checked', true);
        $('#add_hashtag_sunday_check').attr('checked', true);
    };


$(document).ready(function () {
    "use strict";

    $('#hashtag_list').hide();
    $('#no_hashtags_message').hide();
    $('#weekdays_select_div').show();
    $('#disable_hashtag_btn').hide();
    $('#enable_hashtag_btn').hide();

    update_hashtags_status();
    clear_add_hashtag_form();
    load_hashtag_group_table();

    $("#hashtag_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_hashtag_groups_btn').click(function () {
        manage_linked_hashtag_groups();
    });

    $('#save_hashtag_groups_btn').click(function () {
        link_hashtag_groups();
    });

    $('#add_hashtag_btn').click(function () {
        $('#hashtag_modal_title').text("Agregar sufijo");
        $('#hashtag_status_row').hide();
        show_add_hashtag_form();
    });

    $('#close_hashtag_form').click(function () {
        clear_add_hashtag_form();
        load_hashtag_table(true);
    });

    $('#save_hashtag_btn').click(function () {
        if(validate_add_hashtag_form()){
            submit_hashtag();
            clear_add_hashtag_form();
        }else{
            return false;
        }
    });

    $('#add_hashtag_start_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#add_hashtag_end_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#add_hashtag_start_datepicker').datepicker();
    $('#add_hashtag_end_datepicker').datepicker();

    $('#switch_hashtags_btn').click(function () {
        var action = ($("#hashtags_status").val() == "inactive")? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " los sufijos?")) {
            $.post("/hashtags/switch_status/" + $('#current_channel').val(), function (data) {
                update_hashtags_status();
            });
        } else {
            update_hashtags_status();
        }
    });

    $('#disable_hashtag_btn').click(function () {
        if (confirm("Está seguro de que desea desactivar este sufijo?")) {
            disable_hashtag();
        }
    });

    $('#enable_hashtag_btn').click(function () {
        if (confirm("Está seguro de que desea activar este sufijo?")) {
            enable_hashtag();
        }
    });

});