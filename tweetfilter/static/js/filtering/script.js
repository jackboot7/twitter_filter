var
    update_retweets_status = function () {
        "use strict";

        $.get("/filtering/check_status/" + $('#current_channel').val(), function (data) {
            var
                btn = $('#switch_retweets_btn'),
                label = $('#switch_retweets_label');

            if(data.module_enabled){
                btn.attr('title', "Haga click para desactivar");
                label.text("Activo");
                label.removeClass('label-important').addClass('label-success');
                $("#retweets_status").val("active");
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
                $("#retweets_status").val("inactive");
            }

            $('#activate_timeblocks_check').attr('checked', data.scheduled_blocks);
            $('#activate_blacklist_check').attr('checked', data.blacklist);
            $('#activate_triggers_check').attr('checked', data.triggers);
            $('#activate_replacements_check').attr('checked', data.replacements);
            $('#activate_filters_check').attr('checked', data.filters);
            $('#activate_prevent_update_limit_check').attr('checked', data.prevent_update_limit);

            if($('#activate_timeblocks_check').is(":checked")){
                $('#timeblocks_box').fadeIn();

                if (!$('#left_column').is(":visible")){
                    $('#left_column').fadeIn();
                }
            }else{
                $('#timeblocks_box').hide();

                if (!$('#activate_blacklist_check').is(":checked")){
                    $('#left_column').hide();
                }
            }

            if($('#activate_blacklist_check').is(":checked")){
                $('#blocked_user_groups_box').fadeIn();

                if (!$('#left_column').is(":visible")){
                    $('#left_column').fadeIn();
                }
            }else{
                $('#blocked_user_groups_box').hide();

                if (!$('#activate_timeblocks_check').is(":checked")){
                    $('#left_column').hide();
                }
            }

            if($('#activate_filters_check').is(":checked")){
                $('#filter_groups_box').fadeIn();
            }else{
                $('#filter_groups_box').hide();
            }

            if($('#activate_replacements_check').is(":checked")){
                $('#replacement_groups_box').fadeIn();
            }else{
                $('#replacement_groups_box').hide();
            }
 
            if($('#activate_triggers_check').is(":checked")){
                $('#trigger_groups_box').fadeIn();
            }else{
                $('#trigger_groups_box').hide();
            }
        });
    };

$(document).ready(function () {
    "use strict";

    update_retweets_status();

    $('#switch_retweets_btn').click(function () {
        var action = ($("#retweets_status").val() == "inactive")? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " los retweets automáticos?")) {
            $.post("/filtering/switch_status/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_timeblocks_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " la restricción de horarios?")) {
            $.post("/filtering/switch_scheduledblocks/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_blacklist_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " el bloqueo de usuarios?")) {
            $.post("/filtering/switch_blacklist/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_triggers_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " la detección de disparadores?")) {
            $.post("/filtering/switch_triggers/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_replacements_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " los supresores?")) {
            $.post("/filtering/switch_replacements/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_filters_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " los retenedores?")) {
            $.post("/filtering/switch_filters/" + $('#current_channel').val(), function (data) {
                update_retweets_status();
            });
        } else {
            update_retweets_status();
        }
    });

    $("#activate_prevent_update_limit_check").change(function () {
        var action = ($(this).is(":checked"))? "activar" : "desactivar";
        if (confirm("Está seguro de que desea " + action + " la prevención de update limit?")) {
            $.post("/filtering/switch_update_limit/" + $('#current_channel').val(), function (data) {
                // dar feedback?
            });
        } else {
            update_retweets_status();
        }
    });
});
