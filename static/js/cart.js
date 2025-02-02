$(document).ready(function () {
    let orderTotalEle = $('div.order-total').children('p').children('span')
    let cartCountEle = $('a#cart-item-count').children('span.count')
    let itemAdded = $('p.item-added').hide()

    $('.addToCartForm').submit(function (e) {
        e.preventDefault()
        itemAdded.show(500)
        let formData = $(this).serialize()
        arr = formData.split('&')
        if (user === 'AnonymousUser') {
            action = arr[1].split('=')[1]
            variantId = arr[2].split('=')[1]
            // Updating cookie
            updateCookieItem(variantId, action)
            updateCartData()
        } else {

            $.ajax({
                url: '/cart/add-to-cart/',
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
            variantId = arr[1].split('=')[1]
            action = arr[2].split('=')[1]
            updateCookieItem(variantId, action)
            $.ajax({
                url: '/cart/unauth-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    itemTotalEle.text(response['item_total'])
                    let qty = String(response['item_quantity'])
                    qtyEle.text(qty)
                    orderTotalEle.text(response['order_total'])
                    if (response['item_quantity'] == null) {
                        $(thisForm).parents('.cart-item').hide()
                        updateCartData()
                    }
                    if (Object.keys(cart).length === 0) {
                        $('#cart-empty').text('Your cart is empty.')
                    }
                }
            })
        } else {

            $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    // update_cart 
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
        if (user == 'AnonymousUser') {
            let itemTotalEle = $(this).parents('.cart-item').children('div.item-total').children('p').children('span')
            let qtyEle = $(this).siblings('p.qtyBar')

            arr = formData.split('&')
            variantId = arr[1].split('=')[1]
            action = arr[2].split('=')[1]


            updateCookieItem(variantId, action)
            $(this).parents('.cart-item').hide()
            updateCartData()
            $.ajax({
                url: '/cart/updating-cart-total/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    orderTotalEle.text(response['order_total'])
                    if (response['order_total'] <= 0) {
                        $('#cart-empty').text('Your cart is empty.')
                    }
                }
            })
        } else {
            $.ajax({
                url: '/cart/add-to-cart/',
                type: 'POST',
                data: formData,
                success: function (response) {
                    // update_cart 
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
    $('#checkoutBtn').click(function(e){
        e.preventDefault()
        if(Object.keys(cart).length <= 0){
            alert("Can't proceed. Your cart is empty.")
        } else {
            location.href = "/checkout/"
        }
    })
})


function updateCookieItem(variantId, action) {

    if (action == 'add') {
        if (cart[variantId] == undefined) {
            cart[variantId] = { 'quantity': 1}
        } else {
            cart[variantId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[variantId]['quantity'] -= 1

        if (cart[variantId]['quantity'] <= 0) {
            delete cart[variantId]
        }
    }

    if (action == 'delete') {
        delete cart[variantId]
    }


    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

}