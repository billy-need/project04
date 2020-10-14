function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) {
                c_end = document.cookie.length;
            }
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

$(document).ready(() => {

    console.log('document ready...')

    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") },
    });

    $('#searchBtn').click(function () {

        // preparing payload
        var url = "/findstock";
        var stock = $("#stockInput").val();
        var data = "name=" + stock;
        console.log("calling... " + url + " " + data);
        
        // call to server
        $.ajax({
            type: "POST",
            url: url,
            data: data
        })

            .done(function (resp) {
                console.log("Response data:", resp);
                $("#stockName").text(resp);

            })

            .fail(function (resp) {
                console.log("Error:", resp)
                $("#stockName").text("ERROR: " + resp)
            })

    });

});