/**
 * Created by jux on 16-5-10.
 */
var tr_class                = function (journal) {
    // todo: 怎么更优雅的完成组装？模板引擎？
    this.id       = journal.id;
    this.level    = journal.level;
    this.title    = journal.title;
    this.detail   = journal.detail;
    this.datetime = journal.datetime;
    this.html     = '<tr id="' + this.id + '" class="' + ["danger", "warning", "success", "info", "active"][this.level] + '">' +
        '<td>' + this.id + '</td>' +
        '<td>' + this.level + '</td>' +
        '<td>' + this.title + '</td>' +
        '<td>' + this.detail + '</td>' +
        '<td>' + this.datetime + '</td>' +
        '<td>' +
        '<a style="display:block;cursor:hand" href="#">' +
        '<span class="fa fa-pencil-square-o"></span>' +
        '</a>' +
        '<a style="display:block;cursor:hand" href="#">' +
        '<span class="fa fa-trash" data-target="' + this.id + '"></span>' +
        '</a>' +
        '<a style="display: none;cursor:hand" href="#">' +
        '<span class="fa fa-floppy-o" data-target="' + this.id + '"></span>' +
        '</a>' +
        '</td>' +
        '</tr>';
};
var new_action_animation    = function () {
    $("#new_journal").css("display", "none");
    $("#save_journal").css("display", "block");
    $("#cancel_journal").css("display", "block");
    // $("#new_level").css("display", "block");
    $("#new_title").css("display", "block");
    $("#new_detail").css("display", "block");
};
var cancel_action_animation = function () {
    $("#new_journal").css("display", "block");
    $("#new_level").css("display", "none");
    $("#new_title").val("").css("display", "none");
    $("#new_detail").val("").css("display", "none");
    $("#save_journal").css("display", "none");
    $("#cancel_journal").css("display", "none");
};
var edit_record             = function (id, title, detail) {
    $("#edit_" + id).parent().css("display", "none");
    $("#delete_" + id).parent().css("display", "none");
    $("#cancel_" + id).parent().css("display", "block");
    $("#save_" + id).parent().css("display", "block");
    var txt  = "<div class='input-group col-lg-12 col-md-12 col-sm-12 col-xs-12'>" +
            "<input type='text' class='form-control'>" +
            "</div>",
        t_id = "#title_" + id,
        d_id = "#detail_" + id;
    $(t_id).html(txt);
    $(d_id).html(txt);
    $(t_id + " input").val(title);
    $(d_id + " input").val(detail);
};
var get_record              = function (id) {
    var url = "/journal/get/" + id;
    get(url, function (data) {
        $("#" + id).remove();
        var new_tr  = new tr_class(data);
        var id_up   = id + 1,
            id_down = id - 1;
        while (true) {
            var id_d = "#" + id_down,
                id_u = "#" + id_up;
            if ($(id_d).length > 0) {
                $(id_d).prepend(new_tr);
                break;
            } else if ($(id_u).length > 0) {
                $(id_u).append(new_tr);
                break;
            } else {
                id_up += 1;
                id_down -= 1;
            }
        }
    });
};


$(document).ready(function () {
    $("#search").click(function () {
        var param_list         = {},
            url                = "/journal/search/";
        param_list["key_word"] = $("#key_words").val();
        post(url, param_list, function (data) {
                // todo: query success
            },
            function (data) {
                // todo: query error
            });
    });
    $("#new_journal").click(function () {
        new new_action_animation();
    });
    $("#cancel_journal").click(function () {
        new cancel_action_animation();
    });
    $("#save_journal").click(function () {
        var url        = "/journal/new-record/",
            param_list = {
                title : $.trim($("#new_title").val()),
                detail: $.trim($("#new_detail").val()),
                level : 0
            };
        post(url, param_list, function (data) {
                $("#cancel_journal").click();
                var h = new tr_class(data['journal']);
                $("#journal_tbody").prepend(h.html);
            },
            function (data) {
                // todo
            });
    });
    $(".fa-pencil-square-o").click(function () {
        var id     = $(this).data("target"),
            detail = $("#detail_" + id).text(),
            title  = $("#title_" + id).text();
        new edit_record(id, title, detail);
    });
    $(".fa-floppy-o").click(function () {
        var url        = "/journal/update/",
            id         = $(this).data('target'),
            title      = "",
            detail     = "",
            level      = 0,
            param_list = {
                id    : id,
                title : title,
                detail: detail,
                level : level
            };
        var ani        = new waiting();
        $("#" + id).html(ani.html);
        post(url, param_list, function (data) {
            new get_record(id);
        }, function (data) {
            new get_record(id);
        });

    });
    $(".fa-trash").click(function () {
        var url        = "/journal/delete/",
            id         = $(this).data('target'),
            param_list = {id: id};
        post(url, param_list, function (data) {
                if (data['result'] == 'ok') {
                    $("#" + id).detach();
                } else {
                    alert('delete fail');
                }
            },
            function (data) {
            });
    });
});
