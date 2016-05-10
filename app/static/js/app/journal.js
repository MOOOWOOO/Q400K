/**
 * Created by jux on 16-5-10.
 */
function search(param_list) {
    $.ajax({
        type: "post",
        url: "/journal/search/",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(param_list),
        dataType: "json",
        success: function (data) {
        },
        error: function () {
        }
    });
}

$(document).ready(function () {
    $("#search").click(function () {
        var param_list = {},
            key_word = $("#key_words").val();
        param_list["key_word"] = key_word;
        search(param_list);
    });
    $("#new_journal").click(function () {
        $(this).css("display", "none");
        $("#save_journal").css("display", "block");
        $("#cancel_journal").css("display", "block");
        // $("#new_level").css("display", "block");
        $("#new_title").css("display", "block");
        $("#new_detail").css("display", "block");
    });
});
