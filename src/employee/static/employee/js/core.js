$(function () {
    $(".logout").click(function () {
        url = $(this).attr("data-url");
        Swal.fire({
            title: 'Системээс гарах уу?',
            type: 'question',
            showCancelButton: true,
            confirmButtonText: 'Тийм',
            cancelButtonText: 'Үгүй'
        }).then((result) => {
            if (result.value) {
                window.location = url;
            }
        })
    })
})

$(function () {
    $('[data-toggle="deleteAlert"]').click(function () {
        url = $(this).attr("data-href");
        Swal.fire({
            title: "Итгэлтэй байна уу?",
            type: "question",
            showCancelButton: true,
            confirmButtonText: "Тийм",
            cancelButtonText: "Үгүй"
        }).then((result) => {
            if (result.value) {
                window.location = url;
            }
        })
    })
})