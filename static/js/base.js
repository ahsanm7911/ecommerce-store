function updateCartData() {
    let cartCountEle = $('a#cart-item-count').children('span.badge')
    let cart = JSON.parse(getCookie('cart'))
    let cart_length = Object.keys(cart).length
    cartCountEle.text(String(cart_length))
}

$(document).ready(function(){
    let messageDiv = $('.message-div').hide()
    $('#newsletter').submit(function(e){
        e.preventDefault()
        let formData = $(this).serialize()
        $.ajax({
            url: '/newsletter/',
            type: 'POST',
            data: formData,
            success: function(response){
                messageDiv.children('span').text(response)
                messageDiv.show(600)
            }
        })
    })
})