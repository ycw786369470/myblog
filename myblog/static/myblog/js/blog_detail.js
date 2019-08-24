//点击点赞按钮
$('#up').click(function () {
    $.ajax({
        url: '/blog/calc',
        type: 'post',
        data: {
            'mark': 'up',
            // 博主名字
            'blog_name': $('#blog_name #a_name').text(),
            // 点击者名字
            'mark_name': $('#mark_name').text(),
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success:function (res) {
            console.log(res);
            $('#up_num').text(res)
        },
        error:function (error) {
            console.log('访问失败')
        },
    })
});
//点击踩按钮
$('#down').click(function () {
    $.ajax({
        url: '/main/calc/',
        type: 'post',
        data: {
            'mark': 'down',
            'blog_name': $('#blog_name #a_name').text(),
            'mark_name': $('#mark_name').text(),
            'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
        },
        success:function (res) {
            console.log(res);
            $('#down_num').text(res)
        },
        error:function (error) {
            console.log('访问失败')
        },
    })
});
//点击star按钮
// $('#star').click(function () {
//     $.ajax({
//         url: '/main/calc/',
//         type: 'post',
//         data: {
//             'mark': 'star',
//             'blog_name': $('#blog_name #a_name').text(),
//             'mark_name': $('#mark_name').text(),
//             'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
//         },
//         success:function (res) {
//             console.log(res);
//             $('#star_num').text(res)
//         },
//         error:function (error) {
//             console.log(error)
//         },
//     })
// });