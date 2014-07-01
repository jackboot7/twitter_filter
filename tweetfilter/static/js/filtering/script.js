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
            }else{
                btn.attr('title', "Haga click para activar");
                label.text("Desactivado");
                label.removeClass('label-success').addClass('label-important');
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
                $('#blacklist_box').fadeIn();

                if (!$('#left_column').is(":visible")){
                    $('#left_column').fadeIn();
                }
            }else{
                $('#blacklist_box').hide();

                if (!$('#activate_timeblocks_check').is(":checked")){
                    $('#left_column').hide();
                }
            }

            if($('#activate_filters_check').is(":checked")){
                $('#filters_box').fadeIn();
            }else{
                $('#filters_box').hide();
            }

            if($('#activate_replacements_check').is(":checked")){
                $('#replacements_box').fadeIn();
            }else{
                $('#replacements_box').hide();
            }

            if($('#activate_triggers_check').is(":checked")){
                $('#triggers_box').fadeIn();
            }else{
                $('#triggers_box').hide();
            }
        });
    };

$(document).ready(function () {
    "use strict";

    update_retweets_status();

    $('#switch_retweets_btn').click(function () {
        $.post("/filtering/switch_status/" + $('#current_channel').val(), function (data) {
            update_retweets_status();
        });
    });

    $("#activate_timeblocks_check").change(function () {
        $.post("/filtering/switch_scheduledblocks/" + $('#current_channel').val(), function (data) {
            if ($('#activate_timeblocks_check').is(":checked")){
                $('#timeblocks_box').fadeIn();

                if (!$('#left_column').is(":visible")) {
                    $('#left_column').show();
                }
            }else{
                $('#timeblocks_box').fadeOut();

                if (!$('#activate_blacklist_check').is(":checked")) {
                    $('#left_column').hide();
                }
            }
        });
    });

    $("#activate_blacklist_check").change(function () {
        $.post("/filtering/switch_blacklist/" + $('#current_channel').val(), function (data) {
            if ($('#activate_blacklist_check').is(":checked")){
                $('#blacklist_box').fadeIn();

                if (!$('#left_column').is(":visible")) {
                    $('#left_column').show();
                }
            }else{
                $('#blacklist_box').fadeOut();

                if (!$('#activate_timeblocks_check').is(":checked")) {
                    $('#left_column').hide();
                }
            }
        });
    });

    $("#activate_triggers_check").change(function () {
        $.post("/filtering/switch_triggers/" + $('#current_channel').val(), function (data) {
            if ($('#activate_triggers_check').is(":checked")){
                $('#triggers_box').fadeIn();
            }else{
                $('#triggers_box').fadeOut();
            }
        });
    });

    $("#activate_replacements_check").change(function () {
        $.post("/filtering/switch_replacements/" + $('#current_channel').val(), function (data) {
            if($('#activate_replacements_check').is(":checked")){
                $('#replacements_box').fadeIn();
            }else{
                $('#replacements_box').fadeOut();
            }

        });
    });

    $("#activate_filters_check").change(function () {
        $.post("/filtering/switch_filters/" + $('#current_channel').val(), function (data) {
            if($('#activate_filters_check').is(":checked")){
                $('#filters_box').fadeIn();
            }else{
                $('#filters_box').fadeOut();
            }
        });
    });

    $("#activate_prevent_update_limit_check").change(function () {
        $.post("/filtering/switch_update_limit/" + $('#current_channel').val(), function (data) {
            // dar feedback?
        });
    });

    

});
