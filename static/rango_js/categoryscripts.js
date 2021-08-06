$(document).ready(function () {
    $('#sort_views').click(function () {
        if ($('#sort_views').attr("class") == "btn btn-light") {
            $('#sort_views').attr("class", "btn btn-primary")
            $('#sort_like').attr("class", "btn btn-light")
        }
    })
    $('#sort_like').click(function () {
        if ($('#sort_like').attr("class") == "btn btn-light") {
            $('#sort_views').attr("class", "btn btn-light")
            $('#sort_like').attr("class", "btn btn-primary")
        }
    })
})