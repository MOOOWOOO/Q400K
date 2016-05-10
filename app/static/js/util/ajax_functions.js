/**
 * Created by jux on 16-5-11.
 */
function query(method, url, param_list, successCallback, errorCallback) {
    method = method.toLowerCase();
    url = $.trim(url);
    if ((method != "get" && method != "post") || url.length == 0) {
    }
    else {
        $.ajax({
            type: method,
            url: url,
            contentType: "application/json; charset=utf-8",
            data: JSON.stringify(param_list),
            dataType: "json",
            success: function (data) {
                if (typeof data == "string"){
                    data=JSON.parse(data);
                }
                successCallback(data);
            },
            error: function (data) {
                errorCallback(data);
            }
        });
    }
}

