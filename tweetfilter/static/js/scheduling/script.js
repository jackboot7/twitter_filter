var

    send_scheduled_tweet = function (tweet_id) {
        $.post("/scheduling/scheduled_tweet/send/" + tweet_id,
            function (data) {
                if(data.result === "ok") {
                    alert("El tweet fue enviado con éxito");
                }else{
                    alert(data.error_msg);
                }
        });
    },

    delete_scheduled_tweet = function (scheduled_tweet_id) {
        "use strict";

        $.post("/scheduling/scheduled_tweet/delete/" + scheduled_tweet_id, function (data) {
            if(data.result === "ok") {
                load_scheduled_tweet_table(true);
            }
        });
    },

    validate_add_scheduled_tweet_form = function () {
        "use strict";

        if($.trim($('#scheduled_tweet_text').val()) === ""){
            alert("Debe ingresar un texto para la publicación");
            return false;
        }

        if($.trim($('#scheduled_tweet_text').val()).length > 140){
            alert("Debe ingresar un texto menor a 140 caracteres");
            return false;
        }

        if($('#scheduled_tweet_timepicker').val() === ""){
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

    show_add_scheduled_tweet_form = function () {
        $('#scheduled_tweet_table_div').hide();
        $('#add_scheduled_tweet_modal').show();
        $('#scheduled_tweet_group_modal_footer').hide();
    },

    hide_add_scheduled_tweet_form = function () {
        $('#add_scheduled_tweet_modal').hide();
        $('#scheduled_tweet_table_div').show();
        $('#scheduled_tweet_group_modal_footer').show();
    },

    edit_scheduled_tweet = function (scheduled_post) {
        "use strict";

        show_add_scheduled_tweet_form();

        $('#scheduled_tweet_modal_title').text("Editar tweet programado");
        $('#editing_scheduled_tweet_id').val(scheduled_post.id);

        $('#scheduled_tweet_text').val(scheduled_post.text);
        $('#scheduled_tweet_timepicker').val(scheduled_post.time);
        $('#monday_check').attr('checked', scheduled_post.monday);
        $('#tuesday_check').attr('checked', scheduled_post.tuesday);
        $('#wednesday_check').attr('checked', scheduled_post.wednesday);
        $('#thursday_check').attr('checked', scheduled_post.thursday);
        $('#friday_check').attr('checked', scheduled_post.friday);
        $('#saturday_check').attr('checked', scheduled_post.saturday);
        $('#sunday_check').attr('checked', scheduled_post.sunday);

        count_characters();
    },

    manage_linked_scheduled_tweet_groups = function () {
        $.get("/scheduling/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "ScheduledTweet"
        }, function (data) {
            $("#scheduled_tweet_groups_select").multiselect("uncheckAll");        
            $("#scheduled_tweet_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });

            $("#scheduled_tweet_groups_select").multiselect("refresh");
        });
    },

    link_scheduled_tweet_groups = function () {
        var checked_groups = $("#scheduled_tweet_groups_select").val();

        $.post("/scheduling/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "ScheduledTweet"
        }, function (data) {
            load_scheduled_tweet_group_table();
        });
    },

    unlink_scheduled_tweet_group = function(group_id) {
        $.post("/scheduling/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_scheduled_tweet_group_table();
        });
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
                $("#scheduling_status").val("active");
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
                $("#scheduling_status").val("inactive");
            }
        });
    },

    view_scheduled_tweet_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_scheduled_tweet_group_name').html(group_name);
        $('#viewing_scheduled_tweet_group_id').val(group_id);
                
        if (exclusive) {
            //$('#delete_scheduled_tweet_header').show();
            $('#add_scheduled_tweet_btn').show();
        } else {
            //$('#delete_scheduled_tweet_header').hide();
            $('#add_scheduled_tweet_btn').hide();
        }
        
        load_scheduled_tweet_table(exclusive);
    },

    load_scheduled_tweet_group_table = function () {
        "use strict";

        $.get("/scheduling/scheduled_tweet_group/channel/"+$('#current_channel').val(), function (data) {
            $('#scheduled_tweet_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_scheduled_tweet_header').hide();
            } else {
                $('#unlink_scheduled_tweet_header').show();
            }

            $('#scheduled_tweet_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";

                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_scheduled_tweet_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#scheduled_tweet_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_scheduled_tweet_group_modal' data-toggle='modal' id='view_scheduled_tweet_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_scheduled_tweet_group_" + elem.id).click(function () {
                    view_scheduled_tweet_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
                    $('#delete_scheduled_tweet_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_scheduled_tweet_group(elem.id);
                        }
                    });
                }
            });

            $('#scheduled_tweet_group_list_div').slimscroll();
        });
    },

    load_scheduled_tweet_table = function (exclusive) {
        "use strict";

        var delete_btn = "";
        var edit_link = "";
        var static_url = $('#static_url_path').val();

        $.get("/scheduling/scheduled_tweet/list/" + $('#viewing_scheduled_tweet_group_id').val(), function (data) {
            $('#scheduled_tweet_list_tbody').empty();

            if (data.length > 0) {
                $('#no_scheduled_tweets_message').hide();
                $('#scheduled_tweet_list_table').show();

                $.each(data, function (idx, elem) {
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_scheduled_tweet_" + elem.id +"' class='delete_scheduled_tweet' " +
                            "title='Haga click para eliminar el bloque' href='#delete_scheduled_tweet_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                        edit_link = "<a id='edit_scheduled_tweet_" + elem.id + "' href='#' data-toggle='modal'>" + elem.text_excerpt + "</a>";
                    } else {
                        delete_btn = "";
                        edit_link = elem.text_excerpt;
                    }

                    $('#scheduled_tweet_list_tbody').append(
                        "<tr>" +
                            "<td>" + edit_link + "</td>" +
                            "<td>" + elem.date_time + "</td>" +
                            "<td><a id='send_now_" + elem.id + "' class='send_tweet_now no_decoration' " +
                            "title='Haga click para enviar el mensaje ahora' s>"+
                            "<img src='" + static_url + "img/send_now.png'></a></td>" +
                            "<td>" + delete_btn + "</td>" +
                            "</tr>"
                    );

                    if (exclusive) {
                        $('#edit_scheduled_tweet_' + elem.id).click(function () {
                            edit_scheduled_tweet(elem);
                        });

                        $('#delete_scheduled_tweet_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea eliminar el tweet programado seleccionado?")) {
                                delete_scheduled_tweet(elem.id);
                            }
                        });
                    }

                    $('#send_now_' + elem.id).click(function (){
                        $('#sending_now_tweet_text').text(elem.text);
                        if (confirm("Se enviará inmediatamente un mensaje con el texto '" + elem.text +"'...")) {
                            send_scheduled_tweet(elem.id);
                        }
                    });
                });

                $('#scheduled_tweet_list_div').show();
            }else{
                $('#scheduled_tweet_list_div').hide();
                $('#no_scheduled_tweets_message').show();
            }
        });
    },

    /*
    scheduled_tweet_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },
    */

    submit_scheduled_tweet = function () {
        "use strict";

        var url;

        if ($('#editing_scheduled_tweet_id').val()) {
            url = "/scheduling/scheduled_tweet/update/" + $('#editing_scheduled_tweet_id').val();
        }else{
            url = "/scheduling/scheduled_tweet/add/";
        }

        $.post(url, {
            'text':$.trim($('#scheduled_tweet_text').val()),
            'time': $('#scheduled_tweet_timepicker').val(),
            'monday': $('#monday_check').is(':checked') ? 1 : 0,
            'tuesday': $('#tuesday_check').is(':checked') ? 1 : 0,
            'wednesday': $('#wednesday_check').is(':checked') ? 1 : 0,
            'thursday': $('#thursday_check').is(':checked') ? 1 : 0,
            'friday': $('#friday_check').is(':checked') ? 1 : 0,
            'saturday': $('#saturday_check').is(':checked') ? 1 : 0,
            'sunday': $('#sunday_check').is(':checked') ? 1 : 0,
            'group_id': $('#viewing_scheduled_tweet_group_id').val()
        }, function (data) {
            if(data.result === "ok") {
                load_scheduled_tweet_table(true);
            }else{
                //scheduled_post_add_error(data.result);
                alert("hubo un error. Intente de nuevo");
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

        var count = 140 - parseInt($('#scheduled_tweet_text').val().length, 10);
        $('#tweet_char_count').text(count);
        if(count > 20){
            $('#tweet_char_count').css({'color': '#999999'});
        }else if(count <= 10){
            $('#tweet_char_count').css({'color': '#D40D12'});
        }else{
            $('#tweet_char_count').css({'color': '#5C0002'});
        }
    },

    clear_add_scheduled_tweet_form = function () {
        "use strict";

        hide_add_scheduled_tweet_form();

        $('#editing_scheduled_tweet_id').val('');
        $('#scheduled_tweet_timepicker').val('');
        $('#scheduled_tweet_text').val('');

        $('#monday_check').attr('checked', true);
        $('#tuesday_check').attr('checked', true);
        $('#wednesday_check').attr('checked', true);
        $('#thursday_check').attr('checked', true);
        $('#friday_check').attr('checked', true);
        $('#saturday_check').attr('checked', true);
        $('#sunday_check').attr('checked', true);

        count_characters();
    };


$(document).ready(function () {
    "use strict";

    $('#scheduled_tweet_list').hide();
    $('#no_scheduled_tweets_message').hide();
    $('#weekdays_select_div').show();

    update_scheduling_status();
    clear_add_scheduled_tweet_form();
    load_scheduled_tweet_group_table();

    $("#scheduled_tweet_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_scheduled_tweet_groups_btn').click(function () {
        manage_linked_scheduled_tweet_groups();
    });

    $('#save_scheduled_tweet_groups_btn').click(function () {
        link_scheduled_tweet_groups();
    });

    $('#add_scheduled_tweet_btn').click(function () {
        $('#scheduled_tweet_modal_title').text("Agregar tweet programado");
        show_add_scheduled_tweet_form();
    });

    $('#close_scheduled_tweet_form').click(function () {
        clear_add_scheduled_tweet_form();
    });

    $('#save_scheduled_tweet_btn').click(function () {
        if(validate_add_scheduled_tweet_form()){
            submit_scheduled_tweet();
            clear_add_scheduled_tweet_form();
        }else{
            return false;
        }
    });

    $('#scheduled_tweet_timepicker').timepicker({
        hourText: 'Hora',
        minuteText: 'Minutos'
    });

    $('#switch_scheduling_btn').click(function () {
        var action = ($("#scheduling_status").val() == "inactive")? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " los tweets programados?")) {
            $.post("/scheduling/switch_status/" + $('#current_channel').val(), function (data) {
            update_scheduling_status();
        });
        } else {
            update_scheduling_status();
        }
    });

});