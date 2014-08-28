var
    
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
        $('#scheduled_tweet_status_row').show();

        $('#scheduled_tweet_text').val(scheduled_post.text);
        $('#scheduled_tweet_timepicker').val(scheduled_post.time);
        $('#monday_check').attr('checked', scheduled_post.monday);
        $('#tuesday_check').attr('checked', scheduled_post.tuesday);
        $('#wednesday_check').attr('checked', scheduled_post.wednesday);
        $('#thursday_check').attr('checked', scheduled_post.thursday);
        $('#friday_check').attr('checked', scheduled_post.friday);
        $('#saturday_check').attr('checked', scheduled_post.saturday);
        $('#sunday_check').attr('checked', scheduled_post.sunday);

        if (scheduled_post.status == 1) {   // scheduled tweet is enabled
            enable_scheduled_tweet_form();
        } else {
            disable_scheduled_tweet_form();
        }

        count_characters();
    },

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
            'group_id': $('#editing_scheduled_tweet_group_id').val()
        }, function (data) {
            if(data.result === "ok") {
                load_scheduled_tweet_table();
            }else{
                //scheduled_post_add_error(data.result);
                alert("hubo un error. Intente de nuevo");
            }

        });

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
    },

    submit_channels = function () {
        "use strict";
        
        var checked_channels = $("#link_channels_select").val();

        $.post("/scheduling/scheduled_tweet_group/set_channels/" + $('#editing_scheduled_tweet_group_id').val(), {
            'channels': JSON.stringify(checked_channels)
        }, function (data) {
            /*
            if (data.result == "OK") {
                // alert todo bien
            }
            */
        });
    },

    delete_scheduled_tweet = function (scheduled_tweet_id) {
        "use strict";

        $.post("/scheduling/scheduled_tweet/delete/" + scheduled_tweet_id, function (data) {
            if(data.result === "ok") {
                load_scheduled_tweet_table();
            }
        });
    },

    disable_scheduled_tweet_form = function () {
        "use strict";

        // disable fields?
        $("#disable_scheduled_tweet_btn").hide();
        $("#enable_scheduled_tweet_btn").show();
    },

    enable_scheduled_tweet_form = function () {
        "use strict";

        // enable fields?
        $("#enable_scheduled_tweet_btn").hide();
        $("#disable_scheduled_tweet_btn").show();
    },

    enable_scheduled_tweet = function () {
        "use strict";

        $.post("/scheduling/scheduled_tweet/enable/" + $("#editing_scheduled_tweet_id").val(), function (data) {
            if(data.result === "ok") {
                enable_scheduled_tweet_form();
            }
        });
    },

    disable_scheduled_tweet = function () {
        "use strict";

        $.post("/scheduling/scheduled_tweet/disable/" + $("#editing_scheduled_tweet_id").val(), function (data) {
            if(data.result === "ok") {
                disable_scheduled_tweet_form();
            }
        });
    },

    load_scheduled_tweet_table = function () {
        "use strict";

        $.get("/scheduling/scheduled_tweet/list/" + $('#editing_scheduled_tweet_group_id').val(), function (data) {
            $('#scheduled_tweet_list_tbody').empty();

            if (data.length > 0) {
                var modal_body = $($('#add_scheduled_tweet_modal').html());

                $('#no_scheduled_tweets_message').hide();
                $('#scheduled_tweet_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#scheduled_tweet_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_scheduled_tweet_" + elem.id + "' href='#'>" + elem.text_excerpt + "</a></td>" +
                            "<td>" + elem.date_time + "</td>" +
                            "<td><a href='#' id='delete_scheduled_tweet_" + elem.id +"' class='delete_scheduled_tweet' " +
                            "title='Haga click para eliminar tweet programado'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                        "</tr>"
                    );

                    $('#edit_scheduled_tweet_' + elem.id).click(function () {
                        edit_scheduled_tweet(elem);
                    });

                    $('#delete_scheduled_tweet_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea eliminar el tweet programado seleccionado?")) {
                            delete_scheduled_tweet(elem.id);
                        }
                    });
                });

                $('#scheduled_tweet_list_div').slimscroll();
            }else{
                $('#scheduled_tweet_list_table').hide();
                $('#no_scheduled_tweets_message').show();
            }
        });
    },

    edit_scheduled_tweet_group = function (group) {
        "use strict";

        $('#scheduled_tweet_group_modal_title').text("Editar grupo de tweets programados");
        $('#editing_scheduled_tweet_group_id').val(group.id);
        $('#add_scheduled_tweet_group_name').val(group.name);
        $('#scheduled_tweets_box').show();
        $('#save_scheduled_tweet_group_btn').attr('data-dismiss', "modal");

        load_scheduled_tweet_table();
        $('#scheduled_tweet_table_div').show();
    },

    manage_linked_channels = function (group) {
        "use strict";

        $('#editing_scheduled_tweet_group_id').val(group.id);
        
        /*$.each(group.channels, function (index, value) {
            $("#link_channels_select").scheduled_tweet('[value="' + value + '"]').prop('selected', true);
        }); */
        
        $.get("/scheduling/scheduled_tweet_group/list_channels/" + group.id, {}, function (data) {
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

    delete_scheduled_tweet_group = function () {
        "use strict";

        $.post("/scheduling/scheduled_tweet_group/delete/" + $('#deleting_scheduled_tweet_group_id').val(), function (data) {
            if(data.result === "ok") {
                load_scheduled_tweet_group_table();
            }
        });
    },

    load_scheduled_tweet_group_table = function () {
        "use strict";

        var static_url = $('#static_url_path').val();

        $.get("/scheduling/scheduled_tweet_group/list/", function (data) {
            $('#scheduled_tweet_group_list_tbody').empty();
            
            if (data.length > 0) {
                $('#no_scheduled_tweet_groups_message').hide();
                $('#scheduled_tweet_group_list_table').show();

                $.each(data, function (idx, elem) {
                    $('#scheduled_tweet_group_list_tbody').append(
                        "<tr>" +
                            "<td><a id='edit_scheduled_tweet_group_btn_" + elem.id + "' href='#add_scheduled_tweet_group_modal' data-toggle='modal'>" + elem.name + "</a></td>" +
                            "<td class='link_channels_btn'><a class='no_decoration' id='link_channels_" + elem.id + "'" +
                            "title='Haga click para asociar canales al grupo' href='#add_channels_modal' data-toggle='modal'>"+
                            "<img src='" + static_url + "img/add-list-icon.png' class='link_channels_btn'></a></td>" +
                            "<td><a id='delete_scheduled_tweet_group_" + elem.id + "' class='delete_scheduled_tweet_group' " +
                            "title='Haga click para eliminar el grupo' href='#delete_scheduled_tweet_group_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#edit_scheduled_tweet_group_btn_' + elem.id).click(function () {
                        edit_scheduled_tweet_group(elem);
                    });

                    $('#delete_scheduled_tweet_group_' + elem.id).click(function () {
                        $('#deleting_scheduled_tweet_group_id').val(elem.id);
                    });

                    $('#link_channels_' + elem.id).click(function () {
                        manage_linked_channels(elem);
                    });
                });
            }else{
                $('#scheduled_tweet_group_list_table').hide();
                $('#no_scheduled_tweet_groups_message').show();
            }
        });
    },

    clear_add_scheduled_tweet_group_form = function () {
        "use strict";

        $('#editing_scheduled_tweet_group_id').val('');
        $('#add_scheduled_tweet_group_name').val('');
        $('#scheduled_tweets_box').hide();
        $('#save_scheduled_tweet_group_btn').removeAttr("data-dismiss");
    },

    scheduled_tweet_group_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_scheduled_tweet_group = function () {
        "use strict";

        var 
            url,
            new_group = ($('#editing_scheduled_tweet_group_id').val() == "")? true : false;

        if (new_group) {
            url = "/scheduling/scheduled_tweet_group/add/";
        }else{
            url = "/scheduling/scheduled_tweet_group/update/" + $('#editing_scheduled_tweet_group_id').val();
        }

        $.post(url, {
            'scheduled_tweet_group_name': $.trim($('#add_scheduled_tweet_group_name').val()),
        }, function (data) {
            if(data.result == "ok") {
                load_scheduled_tweet_group_table();
                if(new_group){
                    edit_scheduled_tweet_group(data.group_obj);
                }
            }else{
                if (data.result == "duplicate") {
                    alert("Ya existe un grupo con el nombre introducido");
                }
            }
        });

    },

    validate_add_scheduled_tweet_group_form = function () {
        "use strict";

        if($.trim($('#add_scheduled_tweet_group_name').val()) === ""){
            alert("Debe ingresar un nombre para el grupo");
            return false;
        }

        return true;
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
    };

$(document).ready(function () {
    "use strict";

    $('.menu_li').removeClass("active");
    $('#menu_scheduling_li').addClass("active");
    
    clear_add_scheduled_tweet_group_form();
    clear_add_scheduled_tweet_form();
    load_scheduled_tweet_group_table();

    $('#scheduled_tweet_table_div').hide();
    $('#disable_scheduled_tweet_btn').hide();
    $('#enable_scheduled_tweet_btn').hide();

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

    $('#save_scheduled_tweet_group_btn').click(function () {
        if(validate_add_scheduled_tweet_group_form()){
            submit_scheduled_tweet_group();
        }else{
            return false;
        }
    });

    $('#add_scheduled_tweet_group_btn').click(function () {
        $('#scheduled_tweet_group_modal_title').text("Crear grupo de tweets programados");
        clear_add_scheduled_tweet_group_form();
    });


    /*$('#add_channels_modal').click(function () {
        /////
    });*/

    $('#save_channels_btn').click(function () {
        submit_channels();
    });

    $('#delete_scheduled_tweet_group_confirmed').click(function () {
        delete_scheduled_tweet_group();
    });

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });
    
    $('#add_scheduled_tweet_btn').click(function () {
        $('#scheduled_tweet_modal_title').text("Agregar tweet programado");
        $('#scheduled_tweet_status_row').hide();
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

    $('#scheduled_tweet_text').bind("keyup change input", function () {
        count_characters();
    });    

    $("#link_channels_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar canales"
    });

    $('#disable_scheduled_tweet_btn').click(function () {
        if (confirm("Está seguro de que desea desactivar este tweet programado?")) {
            disable_scheduled_tweet();
        }
    });

    $('#enable_scheduled_tweet_btn').click(function () {
        if (confirm("Está seguro de que desea activar este tweet programado?")) {
            enable_scheduled_tweet();
        }
    });
});