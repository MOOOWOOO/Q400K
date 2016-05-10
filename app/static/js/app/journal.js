/**
 * Created by jux on 16-5-10.
 */
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
                console.log(data);
                $("#cancel_journal").click();
                // todo
            },
            function (data) {
                // todo
            })
    })
});
