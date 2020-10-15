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

    $(document).on('keypress', function (e) {
        if (e.which == 13) {
            $('#searchBtn').click()
        }
    });

    // Search for stock by symbol
    $('#searchBtn').click(function () {

        // preparing payload
        var url = "/findstock";
        var stock = $("#stockInput").val();
        var data = "name=" + stock;

        // call to server
        $.ajax({
            type: "POST",
            url: url,
            data: data
        })

            .done(function (resp) {
                var json = $.parseJSON(resp);
                $("#stockOutput").removeClass("hidden");
                console.log("Response data:", json);

                var price = json.price;
                var prevClose = json.close;
                var today = +((prevClose - price).toFixed(2));
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

            .fail(function (resp) {
                var result = $.parseJSON(resp);
                console.log("Error:", result)
                $("#stockName").text("Error: " + result)
            })

    });

    // Buy stocks
    $('#buyBtn').click(() => {

        // preparing payload
        var url = "/buystock";

        var data = {
            symbol: $("#stockSymbol").text(),
            shares: $("#stockShares").val(),
            price: $("#stockPrice").text()
        }

        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (data) {
                console.log("Sucess: " + data)
                $("#plotOutput").removeClass("hidden");
            },
            error: function (data) {
                console.log("Error: " + data)
                $("#result").val("Something went wrong.");
            }
        })
    });

    // Sell stocks
    $('#sellBtn').click(() => {

        // preparing payload
        var url = "/sellstock";

        var data = {
            symbol: $("#stockSymbol").text(),
            shares: $("#stockShares").val(), 
            price: $("#stockPrice").text()
        }

        $.ajax({
            type: "POST",
            url: url,
            dataType: 'json',
            data: JSON.stringify(data),
            success: function (data) {
                console.log("Sucess: " + data)
                $("#result").val(data);
            },
            error: function (data) {
                console.log("Error: " + data)
                $("#result").val("Something went wrong.")
            }
        })
    });

    $('#drawBtn').click(function () {

        // preparing payload
        var url = "/drawstock";
        var stock = $("#stockSymbol").text()
        var data = "name=" + stock;

        // call to server
        $.ajax({
            type: "POST",
            url: url,
            data: data,
            success: function (data) {
                console.log("Sucess: " + data)
                $("#plotOutput").removeClass("hidden");
            },
            error: function (data) {
                console.log("Error: " + data)
            }
        })

    });
    

});
