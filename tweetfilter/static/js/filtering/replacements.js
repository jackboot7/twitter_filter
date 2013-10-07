var
    load_replacement_table = function () {
        "use strict";

        $.get("/filtering/replacement/list/"+$('#current_channel').val(), function (data) {
            $('#replacement_list_tbody').empty();

            if (data.length > 0) {
                $('#no_replacements_message').hide();
                $('#replacement_list_table').show();
                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {

                    $('#replacement_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + elem.replace_with + "</td>" +
                            "<td><div class='offset2'>" + "<input id='replacement_mention_check_" + elem.id +
                            "' type='checkbox' checked='"  + elem.enabled_mentions + "'></div></td>" +
                            "<td><div class='offset2'><input id='replacement_mention_check_" + elem.id +
                            "' type='checkbox' checked='"  + elem.enabled_dm + "'></div></td>" +
                            "<td><div class='offset2'><a id='delete_replacement_" + elem.id +"' class='delete_replacement' " +
                            "title='Haga click para eliminar el supresor' href='#delete_replacement_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</div></td>" +
                            "</tr>"
                    );

                    $('#delete_replacement_' + elem.id).click(function () {
                        $('#deleting_replacement_text').text(elem.text);
                        $('#deleting_replacement_id').val(elem.id);
                    });
                });

                $('#replacement_list_div').slimscroll();
            }else{
                $('#replacement_list_table').hide();
                $('#no_replacements_message').show();
            }
        });
    },

    replacement_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    submit_new_replacement = function () {
        "use strict";

        var replacement_text = $.trim($('#add_replacement_text').val()),
            replace_with = $.trim($('#add_replacement_replace_with').val());

        if(replacement_text.length > 0) {
            $.post("/filtering/replacement/add/", {
                'replacement_text': replacement_text,
                'replacement_replace_with': replace_with,
                'replacement_channel': $('#current_channel').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_replacement_text').val("");
                    $('#add_replacement_replace_with').val("");
                    load_replacement_table();
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    replacement_add_error(data.result);
                }
            });
        }
    };

$(document).ready(function () {
    "use strict";

    $('#replacement_list_table').hide();
    $('#no_replacements_message').hide();

    load_replacement_table();

    $('#delete_replacement_confirmed').click(function () {
        $.post("/filtering/replacement/delete/" + $('#deleting_replacement_id').val(), function (data) {
            if(data.result === "ok") {
                load_replacement_table();
            }
        });
    });

    $('#add_replacement_btn').click(function () {
        submit_new_replacement();
    });

    $('#add_replacement_text').keypress(function (e) {
        if (e.which === 13) {
            $('#add_replacement_replace_with').focus();
        }
    });

    $('#add_replacement_replace_with').keypress(function (e) {
        if (e.which === 13) {
            submit_new_replacement();
        }
    });
});