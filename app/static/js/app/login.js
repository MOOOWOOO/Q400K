/**
 * Created by jux on 16-3-21.
 */

$(document).ready(function () {
    $("#login").click(function () {
        user_info=JSON.stringify({
                "username": $("#username").val(),
                "password": $("#password").val()
            });
        $.ajax({
            type: "post",
            data: user_info,
            url: "/login/",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function (data) {
                switch (data["code"]){
                    case 1:
                        break;
                    case 2:
                        $("#message").text(data["msg"]);
                        break;
                }
            }
        });
    });
});
