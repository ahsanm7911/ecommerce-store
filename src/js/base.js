function updateCartData() {
    let cartCountEle = $('a#cart-item-count').children('span.badge')
    let cart = JSON.parse(getCookie('cart'))
    let cart_length = Object.keys(cart).length
    cartCountEle.text(String(cart_length))
}
