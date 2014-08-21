var
    
    manage_linked_filter_groups = function () {
               
        $.get("/filtering/channel/list_groups/" + $("#current_channel").val(), {
            'content_type': "Filter"
        }, function (data) {
            $("#filter_groups_select").multiselect("uncheckAll");        
            $("#filter_groups_select").multiselect("widget").find(":checkbox").each(function(){
                var widget = this;
                $.each(data, function (index, value) {
                    if (widget.value == value) {
                        widget.click();
                    }
                });
            });
            $("#filter_groups_select").multiselect("refresh");
        });
    },

    unlink_filter_group = function(group_id) {
        $.post("/filtering/channel/unlink_group/" + $('#current_channel').val(), {
            'group_id': group_id
        }, function (data) {
            load_filter_group_table();
        });
    },

    link_filter_groups = function () {
        var checked_groups = $("#filter_groups_select").val();

        $.post("/filtering/channel/set_groups/" + $('#current_channel').val(), {
            'groups': JSON.stringify(checked_groups),
            'content_type': "Filter"
        }, function (data) {
            load_filter_group_table();
        });
    },

    delete_filter = function (filter_id) {
        $.post("/filtering/filter/delete/" + filter_id, function (data) {
            if(data.result === "ok") {
                load_filter_table(true);
            }
        });
    },

    load_filter_table = function (exclusive) {
        "use strict";

        var delete_btn = "";

        $.get("/filtering/filter/list/" + $('#viewing_filter_group_id').val(), function (data) {
            $('#filter_list_tbody').empty();

            if (data.length > 0) {
                $('#no_filters_message').hide();
                $('#filter_list_table').show();

                $.each(data, function (idx, elem) {
                    if (exclusive) {
                        delete_btn = 
                            "<a id='delete_filter_" + elem.id +"' class='no_decoration' " +
                            "title='Haga click para eliminar retenedor'>" +
                            "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                    } else {
                        delete_btn = "";                        
                    }

                    $('#filter_list_tbody').append(
                        "<tr>" +
                            "<td>" + elem.text + "</td>" +
                            "<td>" + delete_btn + "</td>" +
                        "</tr>"
                    );

                    if (exclusive) {
                        $('#delete_filter_' + elem.id).click(function () {
                            if (confirm("Está seguro de que desea eliminar el retenedor seleccionado?")) {
                                delete_filter(elem.id);
                            }
                        });
                    }
                });
                $('#filter_list_div').slimscroll();
            }else{
                $('#filter_list_table').hide();
                $('#no_filters_message').show();
            }
        });
    },

    submit_new_filter = function () {
        "use strict";

        var filter_text = $.trim($('#add_filter_text').val());
        if(filter_text.length > 0) {
            $.post("/filtering/filter/add/", {
                'filter_text': filter_text,
                'group_id': $('#viewing_filter_group_id').val()
            }, function (data) {
                if(data.result === "ok") {
                    $('#add_filter_text').val("");
                    load_filter_table(true);
                }else if(data.result === "duplicate"){
                    alert("La palabra introducida ya existe en la lista");
                }else{
                    alert(data.result);
                    //filter_add_error(data.result)
                }
            });
        }
    },

    view_filter_group = function (group_id, group_name, exclusive) {
        "use strict";

        $('#viewing_filter_group_name').html(group_name);
        $('#viewing_filter_group_id').val(group_id);

        if (exclusive) {
            $('#delete_filter_header').show();
            $('#add_filter_btn_table').show();
        } else {
            $('#delete_filter_header').hide();
            $('#add_filter_btn_table').hide();
        }
                
        load_filter_table(exclusive);
    },

    load_filter_group_table = function () {
        "use strict";

        $.get("/filtering/filter_group/channel/"+$('#current_channel').val(), function (data) {
            $('#filter_group_list_tbody').empty();

            if (data.length == 1) {
                $('#unlink_filter_header').hide();
            } else {
                $('#unlink_filter_header').show();
            }

            $('#filter_group_list_table').show();

            $.each(data, function (idx, elem) {
                var unlink_button = "";
                if (!elem.channel_exclusive)  {
                    unlink_button = 
                        "<a id='delete_filter_group_" + elem.id +"' class='no_decoration' " +
                        "title='Haga click para desvincular el grupo'>" +
                        "<span class='badge badge-important' contenteditable='false'>x</span></a>";
                }

                $('#filter_group_list_tbody').append(
                    "<tr>" +
                        "<td><a href='#view_filter_group_modal' data-toggle='modal' id='view_filter_group_" + elem.id + "'>" + elem.name + "</a></td>" +
                        "<td>" + unlink_button + "</td>" +
                    "</tr>"
                );

                $("#view_filter_group_" + elem.id).click(function () {
                    view_filter_group(elem.id, elem.name, elem.channel_exclusive);
                });

                if (!elem.channel_exclusive) {
                    $('#delete_filter_group_' + elem.id).click(function () {
                        if (confirm("Está seguro de que desea desvincular este canal del grupo seleccionado?")) {
                            unlink_filter_group(elem.id);
                        }
                    });
                }
            });

            $('#filter_group_list_div').slimscroll();
        });
    },

    // Wat?
    filter_add_error = function (text) {
        "use strict";

        $('#alert_warning_body').text(text);
        $('#alert_warning').show();
    };

$(document).ready(function () {
    "use strict";

    load_filter_group_table();

    
    $('#delete_filter_confirmed').click(function () {
        $.post("/filtering/filter/delete/" + $('#deleting_filter_id').val(), function (data) {
            if(data.result === "ok") {
                load_filter_table(true);
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

    $("#filter_groups_select").multiselect({
       selectedText: "# de # seleccionados",
       checkAllText: "Todos",
       uncheckAllText: "Ninguno",
       noneSelectedText: "Seleccionar grupos"
    });

    $('#link_filter_groups_btn').click(function () {
        manage_linked_filter_groups();
    });

    $('#save_filter_groups_btn').click(function () {
        link_filter_groups();
    });
    
});