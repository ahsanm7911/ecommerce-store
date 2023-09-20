$(document).ready(function () {

    $imageWrapper = $('.image-wrapper')
    $imageWrapper.hover(function (e) {
        e.preventDefault()
        $(this).children('.hover-effect').toggleClass('d-none')

    })
})
