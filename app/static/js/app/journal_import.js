/**
 * Created by jux on 16-5-31.
 */
$(document).ready(function () {
    var form     = $("#upload-form"),
        progress = $("#uploadprogress"),
        holder   = $("#holder");
    form.on(function () {
        if (window.FormData) {
            var form_data = new FormData();
            form_data.append('upload', $("#upload").files[0]);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', $(this).attr('action'));
            xhr.onload = function () {
                if (xhr.status === 200) {
                    console.log('OK');
                } else {
                    console.log('ERR');
                }
            };
            xhr.send(form_data);
            xhr.upload.onprogress = function (event) {
                if (event.lengthComputable) {
                    var complete = (event.loaded / event.total * 100 | 0);

                    progress.value = progress.innerHTML = complete;
                }
            };
        }
    });
});