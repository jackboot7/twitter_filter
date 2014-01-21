var

    load_filter_table = function () {
        "use strict";

        $.get("/filtering/filter/list/"+$('#current_channel').val(), function (data) {
            $('#filter_list_tbody').empty();

            if (data.length > 0) {
                $('#no_filters_message').hide();
                $('#filter_list_table').show();
                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {
                    $('#filter_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            /*
                            "<td><div class='offset2'><input id='filter_mention_check_" + elem.id +
                            "' type='checkbox' checked='"  + elem.enabled_mentions + "'></div></td>" +
                            "<td><div class='offset1'><input id='filter_dm_check_" + elem.id +
                            "' type='checkbox' checked='"  + elem.enabled_dm + "'></div></td>" +
                            */
                            "<td><a id='delete_filter_" + elem.id +"' class='delete_filter' " +
                            "title='Haga click para eliminar filtro' href='#delete_filter_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );
                    /*
                    $('#filter_mention_check_' + elem.id).attr('checked', elem.enabled_mentions);
                    $('#filter_dm_check_' + elem.id).attr('checked', elem.enabled_dm);

                    $('#filter_mention_check_' + elem.id).change(function () {
                        $.post("/filtering/filter/switch_mention/" + elem.id, function () {

                        });
                    });

                    $('#filter_dm_check_' + elem.id).change(function () {
                        $.post("/filtering/filter/switch_dm/" + elem.id, function () {

                        });
                    });
                    // */

                    $('#delete_filter_' + elem.id).click(function () {
                        $('#deleting_filter_text').text(elem.text);
                        $('#deleting_filter_id').val(elem.id);
                    });
                });
                $('#filter_list_div').slimscroll();
            }else{
                $('#filter_list_table').hide();
                $('#no_filters_message').show();
            }
        });
    },

    filter_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_new_filter = function () {
        "use strict";

        var filter_text = $.trim($('#add_filter_text').val());
        if(filter_text.length > 0){
            $.post("/filtering/filter/add/", {
                'filter_text': filter_text,
                'filter_channel': $('#current_channel').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_filter_text').val("");
                    load_filter_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    filter_add_error(data.result);
                }
            });
        }
    };

$(document).ready(function () {
    "use strict";

    $('#filter_list_table').hide();
    $('#no_filters_message').hide();

    load_filter_table();

    $('#delete_filter_confirmed').click(function () {
        $.post("/filtering/filter/delete/" + $('#deleting_filter_id').val(), function (data) {
            if(data.result === "ok") {
                load_filter_table();
            }
        });
    });

    $('#add_filter_btn').click(function () {
        submit_new_filter();
    });

    $('#add_filter_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_filter();
        }
    });
});