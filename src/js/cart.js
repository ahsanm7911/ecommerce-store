console.log('Cart working...')
$(document).ready(function () {
    let cartCountEle = $('a#cart-item-count').children('span.badge')
    let orderTotalEle = $('div.order-total').children('p').children('span')

    $('.addToCartForm').submit(function (e) {
        e.preventDefault()

        let formData = $(this).serialize()
        console.log(formData)
        if (user === 'AnonymousUser') {
            // Updating cookie
            arr = formData.split('&')
            console.log(arr)
            color = arr[1].split('=')[1]
            productId = arr[2].split('=')[1]
            action = arr[3].split('=')[1]
            updateCookieItem(productId, action, color)
            updateCartData(cartCountEle)
        } else {

            $.ajax({
                url: '/add-to-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    cartCountEle.text(response['item_count'])
                }
            })
        }
    })

    $('.qtyForm').submit(function (e) {
        e.preventDefault()

        let formData = $(this).serialize()
        let thisForm = $(this)
        let qtyEle = $(this).siblings('p.qtyBar')
        let itemTotalEle = $(this).parents('.cart-item').children('div.item-total').children('p').children('span')

        if (user == "AnonymousUser") {
            arr = formData.split('&')
            color = arr[1].split('=')[1]
            productId = arr[2].split('=')[1]
            action = arr[3].split('=')[1]

            updateCookieItem(productId, action, color)
            $.ajax({
                url: '/unauth-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    console.log(response)
                    itemTotalEle.text(response['item_total'])
                    let qty = String(response['item_quantity'])
                    qtyEle.text(qty)
                    orderTotalEle.text(response['order_total'])
                    if (response['item_quantity'] == null) {
                        console.log('Hiding cart-item')
                        $(thisForm).parents('.cart-item').hide()
                        updateCartData()
                    }
                    if (Object.keys(cart).length === 0) {
                        console.log('Cart is empty.')
                        $('#cart-empty').text('Your cart is empty.')
                    }
                }
            })
        } else {

            $.ajax({
                url: '/add-to-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    // update_cart 
                    console.log(response)
                    if (response['qty'] <= 0) {
                        $(thisForm).parents('.cart-item').hide()
                    } else {
                        let qty = String(response['qty'])
                        qtyEle.text(qty)
                        itemTotalEle.text(response['item_total'])
                    }
                    if (response['item_count'] <= 0) {
                        $('#cart-empty').text('Your cart is empty.')
                    }
                    cartCountEle.text(response['item_count'])
                    orderTotalEle.text(response['order_total'])
                }
            })
        }
    })

    $('.item-delete-btn').submit(function (e) {
        e.preventDefault()
        let thisForm = $(this)
        let formData = $(this).serialize()
        console.log(formData)
        if (user == 'AnonymousUser') {
            let itemTotalEle = $(this).parents('.cart-item').children('div.item-total').children('p').children('span')
            let qtyEle = $(this).siblings('p.qtyBar')

            arr = formData.split('&')
            color = arr[1].split('=')[1]
            productId = arr[2].split('=')[1]
            action = arr[3].split('=')[1]


            updateCookieItem(productId, action, color)
            $(this).parents('.cart-item').hide()
            updateCartData()
            $.ajax({
                url: 'updating-cart-total/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    orderTotalEle.text(response['order_total'])
                    if (response['order_total'] <= 0) {
                        $('#cart-empty').text('Your cart is empty.')
                    }
                    console.log(response)
                }
            })
        } else {
            $.ajax({
                url: '/add-to-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    // update_cart 
                    console.log(response)
                    $(thisForm).parents('.cart-item').hide()

                    if (response['item_count'] <= 0) {
                        $('#cart-empty').text('Your cart is empty.')
                    }
                    cartCountEle.text(response['item_count'])
                    orderTotalEle.text(response['order_total'])
                }
            })
        }
    })

    function updateCartData() {
        let cart = JSON.parse(getCookie('cart'))
        let cart_length = Object.keys(cart).length
        cartCountEle.text(String(cart_length))
    }

})


function updateCookieItem(productId, action, color) {
    console.log("not logged in...")

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1, 'color': color }
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }

    if (action == 'delete') {
        delete cart[productId]
    }


    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

}