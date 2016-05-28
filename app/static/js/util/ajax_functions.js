/**
 * Created by jux on 16-5-11.
 */
function post(url, param_list, successCallback, errorCallback) {
    url = $.trim(url);
    if (url.length == 0) {
    }
    else {
        $.ajax({
            type       : "post",
            url        : url,
            contentType: "application/json; charset=utf-8",
            data       : JSON.stringify(param_list),
            dataType   : "json",
            success    : function (data) {
                if (typeof data == "string") {
                    data = JSON.parse(data);
                }
                successCallback(data);
            },
            error      : function (data) {
                errorCallback(data);
            }
        });
    }
}

function get(url, successCallback, errorCallback) {
    url = $.trim(url);
    if (url.length == 0) {
    }
    else {
        $.ajax({
            type       : "get",
            url        : url,
            contentType: "application/json; charset=utf-8",
            success    : function (data) {
                if (typeof data == "string") {
                    data = JSON.parse(data);
                }
                successCallback(data);
            },
            error      : function (data) {
                errorCallback(data);
            }
        });
    }
}
