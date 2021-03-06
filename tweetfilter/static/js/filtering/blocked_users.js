var

    load_blocked_user_table = function () {
        "use strict";

        $.get("/filtering/blocked_user/list/"+$('#current_channel').val(), function (data) {
            $('#blocked_user_list_tbody').empty();

            if (data.length > 0) {
                $('#no_blocked_users_message').hide();
                $('#blocked_user_list_table').show();
                //alert(JSON.stringify(data));
                $.each(data, function (idx, elem) {

                    $('#blocked_user_list_tbody').append(
                        "<tr>" +
                            "<td>@" + elem.screen_name + "</td>" +
                            "<td><a id='delete_blocked_user_" + elem.screen_name +"' class='delete_blocked_user' " +
                            "title='Haga click para desbloquear al usuario' href='#delete_blocked_user_confirm_modal' data-toggle='modal'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>" + "</td>" +
                            "</tr>"
                    );

                    $('#delete_blocked_user_' + elem.screen_name).click(function () {
                        $('#deleting_blocked_user_name').text(elem.screen_name);
                        $('#deleting_blocked_user_id').val(elem.id);
                    });
                });
                $('#blocked_user_list_div').slimscroll();
            }else{
                $('#blocked_user_list_table').hide();
                $('#no_blocked_users_message').show();
            }
        });
    },

    blocked_user_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    },

    validate_new_blocked_user = function () {
        "use strict";

        return (/^[a-zA-Z0-9_]{1,15}$/g).test($('#add_blocked_user_name').val());
    },

    submit_new_blocked_user = function () {
        "use strict";

        var screen_name = $.trim($('#add_blocked_user_name').val());

        if(!validate_new_blocked_user()){
            alert("El nombre de la cuenta no debe contener arroba (@) ni otros caracteres especiales");
            return false;
        }

        if(screen_name.length > 0) {
            $.post("/filtering/blocked_user/add/", {
                'blocked_user_name': screen_name,
                'blocked_user_channel': $('#current_channel').val()
            }, function (data) {
                if(data.result === "ok") {
                    load_blocked_user_table();
                    $('#add_blocked_user_name').val('');
                }else if(data.result === "duplicate"){
                    alert("El nombre de cuenta introducido ya existe en la lista");
                }else{
                    blocked_user_add_error(data.result);
                }
            });
        }
    };

$(document).ready(function () {
    "use strict";

    $('#blocked_user_list_table').hide();
    $('#no_blocked_users_message').hide();

    load_blocked_user_table();

    $('#delete_blocked_user_confirmed').click(function () {
        $.post("/filtering/blocked_user/delete/" + $('#deleting_blocked_user_id').val(), function (data) {
            if(data.result === "ok") {
                load_blocked_user_table();
            }
        });
    });

    $('#add_blocked_user_btn').click(function () {
        submit_new_blocked_user();
    });

    $('#add_blocked_user_name').keypress(function (e) {
        if (e.which === 13) {
            submit_new_blocked_user();
        }
    });
});