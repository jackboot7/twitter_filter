var
    
    manage_linked_groups = function (group) {
               
        $.get("/filtering/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "Replacement"
        }, function (data) {
            $("#link_replacement_groups_select").multiselect("uncheckAll");        
            $("#link_replacement_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });
            $("#link_replacement_groups_select").multiselect("refresh");
        });
    },

    unlink_replacement_group = function(group_id) {
        $.post("/filtering/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_trigger_group_table();
        });
    },

    link_replacement_groups = function () {
        var checked_groups = $("#replacement_groups_select").val();

        $.post("/filtering/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "Replacement"
        }, function (data) {
            load_replacement_group_table();
        });
    },

    delete_replacement = function (replacement_id) {
        $.post("/filtering/replacement/delete/" + replacement_id, function (data) {
            if(data.result === "ok") {
                load_replacement_table(true);
            }
        });
    },

    load_replacement_table = function (exclusive) {
        "use strict";

        var delete_btn = "";

        $.get("/filtering/replacement/list/" + $('#viewing_replacement_group_id').val(), function (data) {
            $('#replacement_list_tbody').empty();

            if (data.length > 0) {
                $('#no_replacements_message').hide();
                $('#replacement_list_table').show();

                $.each(data, function (idx, elem) {
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_replacement_" + elem.id +"' class='no_decoration' " +
                            "title='Haga click para eliminar supresor'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                        $('#delete_replacement_header').show();
                        $('#add_replacement_btn_table').show();
                    } else {
                        delete_btn = "";                        
                        $('#delete_replacement_header').hide();
                        $('#add_replacement_btn_table').hide();
                    }

                    $('#replacement_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + elem.replace_with + "</td>" +
                            "<td>" + delete_btn + "</td>" +
                        "</tr>"
                    );

                    if (exclusive) {
                        $('#delete_replacement_' + elem.id).click(function () {
                            if (confirm("Está seguro de que desea eliminar el supresor seleccionado?")) {
                                delete_replacement(elem.id);
                            }
                        });
                    }
                });
                $('#replacement_list_div').slimscroll();
            }else{
                $('#replacement_list_table').hide();
                $('#no_replacements_message').show();
            }
        });
    },

    submit_new_replacement = function () {
        "use strict";

        var replacement_text = $.trim($('#add_replacement_text').val());
        if(replacement_text.length > 0) {
            $.post("/filtering/replacement/add/", {
                'replacement_text': replacement_text,
                'group_id': $('#viewing_replacement_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_replacement_text').val("");
                    load_replacement_table(true);
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                }
            });
        }
    },

    view_replacement_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_replacement_group_name').html(group_name);
        $('#viewing_replacement_group_id').val(group_id);
                
        load_replacement_table(exclusive);
    },

    load_replacement_group_table = function () {
        "use strict";

        $.get("/filtering/replacement_group/channel/"+$('#current_channel').val(), function (data) {
            $('#replacement_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_replacement_header').hide();
            } else {
                $('#unlink_replacement_header').show();
            }

            $('#replacement_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";
                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_replacement_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#replacement_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_replacement_group_modal' data-toggle='modal' id='view_replacement_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_replacement_group_" + elem.id).click(function () {
                    view_replacement_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
                    $('#delete_replacement_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_replacement_group(elem.id);
                        }
                    });
                }
            });

            $('#replacement_group_list_div').slimscroll();
        });
    };

$(document).ready(function () {
    "use strict";

    load_replacement_group_table();

    
    $('#delete_replacement_confirmed').click(function () {
        $.post("/filtering/replacement/delete/" + $('#deleting_replacement_id').val(), function (data) {
            if(data.result === "ok") {
                load_replacement_table(true);
            }
        });
    });

    $('#add_replacement_btn').click(function () {
        submit_new_replacement();
    });

    $('#add_replacement_text').keypress(function (e) {
        if (e.which === 13) {
            submit_new_replacement();
        }
    });

    $("#replacement_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_replacement_groups_btn').click(function () {
        manage_linked_groups();
    });

    $('#save_replacement_groups_btn').click(function () {
        link_replacement_groups();
    });
    
});