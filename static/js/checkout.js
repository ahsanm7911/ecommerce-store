console.log('Checkout js working...')

$(document).ready(function(){
    $('#checkoutForm').submit(function(e){
        e.preventDefault()

        let formData = $(this).serialize()

        $.ajax({
            url: 'process-checkout/',
            type: 'POST',
            data: formData,
            success: function(response){
                console.log('Transaction complete!')
                cart = {}
                document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
                window.location.href = "/"
            }
        })
    })
})