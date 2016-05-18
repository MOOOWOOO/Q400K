/**
 * Created by jux on 16-5-10.
 */
function tr_class(journal) {
    // todo: 怎么更优雅的完成组装？模板引擎？
    this.id=journal.id;
    this.level=journal.level;
    this.title=journal.title;
    this.detail=journal.detail;
    this.datetime=journal.datetime;
    this.html='<tr id="'+this.id+'" class="'+ ["danger", "warning", "success", "info", "active"][this.level] +'">'+
                    '<td>'+this.id+'</td>'+
                    '<td>'+this.level+'</td>'+
                    '<td>'+this.title+'</td>'+
                    '<td>'+this.detail+'</td>'+
                    '<td>'+this.datetime+'</td>'+
                    '<td>'+
                        '<a style="display:block;cursor:hand" href="#">'+
                            '<span class="fa fa-pencil-square-o"></span>'+
                        '</a>'+
                        '<a style="display:block;cursor:hand" href="#">'+
                            '<span class="fa fa-trash" data-target="'+this.id+'"></span>'+
                        '</a>'+
                        '<a style="display: none;cursor:hand" href="#">'+
                            '<span class="fa fa-floppy-o" data-target="'+this.id+'"></span>'+
                        '</a>'+
                    '</td>'+
                '</tr>';
}

$(document).ready(function () {
    $("#search").click(function () {
        var param_list = {},
            key_word = $("#key_words").val(),
            url = "/journal/search/";
        param_list["key_word"] = key_word;
        query("post", url, param_list, function (data) {
                // todo: query success
            },
            function (data) {
                // todo: query error
            });
    });
    $("#new_journal").click(function () {
        $("#new_journal").css("display", "none");
        $("#save_journal").css("display", "block");
        $("#cancel_journal").css("display", "block");
        // $("#new_level").css("display", "block");
        $("#new_title").css("display", "block");
        $("#new_detail").css("display", "block");
    });
    $("#cancel_journal").click(function () {
        $("#new_journal").css("display", "block");
        $("#new_level").css("display", "none");
        $("#new_title").val("").css("display", "none");
        $("#new_detail").val("").css("display", "none");
        $("#save_journal").css("display", "none");
        $("#cancel_journal").css("display", "none");
    });
    $("#save_journal").click(function () {
        var url = "/journal/new-record/",
            param_list = {
                title: $.trim($("#new_title").val()),
                detail: $.trim($("#new_detail").val()),
                level: 0
            };
        query("post", url, param_list, function (data) {
                $("#cancel_journal").click();
                h=new tr_class(data['journal']);
                $("#journal_tbody").prepend(h.html);
            },
            function (data) {
                // todo
            })
    });
    $(".fa-pencil-square-o").click(function () {
        $(this).data('target');
    });
    $(".fa-floppy-o").click(function () {
        $(this).data('target');
    });
    $(".fa-trash").click(function () {
        var url = "/journal/delete/",
            id = $(this).data('target'),
            param_list = {id: id};
        query("post", url, param_list, function (data) {
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
