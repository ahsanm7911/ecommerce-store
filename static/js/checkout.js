$(document).ready(function () {
    let orderCompleteContainer = $('div#orderCompleteContainer')
    orderCompleteContainer.addClass('d-none')

    let checkoutContainer = $('div#checkoutContainer')
    let orderId = $('span.order-id')


    $('#checkoutForm').submit(function (e) {
        e.preventDefault()
        if (Object.keys(cart).length <= 0) {
            alert("Can't proceed. Your cart is empty.")
        } else {

            let formData = $(this).serialize()

            $.ajax({
                url: 'process-checkout/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    cart = {}
                    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
                    checkoutContainer.hide()
                    orderCompleteContainer.removeClass('d-none');
                    orderId.text(response)
                    updateCartData()
                }
            })
        }
    })
})