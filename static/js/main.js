function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$('#make-map').click(function (e) {
    e.preventDefault();
    var endpoint = $("#make-map").attr("data-url");
    console.log(endpoint)
    // $("#loading").show()
    // $("#carp-map-1").hide()
    // $("#carp-map-2").hide()
    // $("#carp-icon").hide()
    $.ajax({
        type: "POST",
        url: endpoint,
        data: {
            year: $('#select_year').val(),
            month:$('#select_month').val(),
            ntop: $('#get_top').val(),
            csrfmiddlewaretoken: getCookie('csrftoken'),
            dataType: "json",
        },
        success: function (data) {
            // $("#loading").hide()
            $("body").html(data)
        },
    });
});

// $('#get-map').click(function (e) {
//     e.preventDefault();
//     var endpoint = $("#get-map").attr("data-url");
//     $.ajax({
//         type: "POST",
//         url: endpoint,
//         data: {
//             file_path: $('#get-map').val(),
//             csrfmiddlewaretoken: getCookie('csrftoken'),
//             dataType: "json",
//             xhrFields: {
//                 responseType: 'blob'
//             },
//         },
//         success: function (data) {
//             let a = document.createElement('a');
//             a.download = "sankey.html";
//             a.href = "data:application/octet-stream;base64," + btoa(data);
//             a.click();
//             a.remove();
//         },
//     });
// });






