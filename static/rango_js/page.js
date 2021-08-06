$('#page_id').onclick(function () {
    var title=request.page.title
    $.ajax({
        url: '/ajax/like_count/',
        data: {'page_title': title, },
        dataType: 'json',
        success: function (data) {
            $('#like_count').repalceWith(data.likes)
        }
    });
})
$('#view_count').onclick(function () {
    var title=request.page.title
    $.ajax({
        url: '/ajax/view_count/',
        data: {'page_title': title, },
        dataType: 'json',
        success: function (data) {
            $('#view_count').repalceWith(data.views)
        }
    });
})