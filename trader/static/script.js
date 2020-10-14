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

    $(document).on('keypress',function(e) {
        if(e.which == 13) {
            $('#searchBtn').click()
        }
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

            .done(function (data) {
                var json = $.parseJSON(data);
                $("#stockOutput").removeClass("hidden");
                console.log("Response data:", json);

                var price = json.price;
                var prevClose = json.close;
                var today = +((prevClose - price).toFixed(2));
                console.log(today);
                $("#stockName").text(json.name);
                $("#stockSymbol").text(json.symbol);
                $("#stockPrice").text(json.price);
                $("#stockToday").text(today);
                $("#stockHigh").text(json.high);
                $("#stockLow").text(json.low);
                // $("#stockVolume").text(json.volume);
                // $("#stockCap").text(json.marketCap);
                // $("#stockfiftyTwoHigh").text(json.fiftyTwoHigh);
                // $("#stockfiftyTwoLow").text(json.fiftyTwoLow);

            })

            .fail(function (data) {
                console.log("Error:", data)
                $("#stockName").text("ERROR: " + data)
            })

    });

});