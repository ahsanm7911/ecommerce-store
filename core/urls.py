from django.urls import path
from . import views
# urlpatterns here

urlpatterns = [

    # SEO
    path('robots.txt', views.robots_txt),

    # Main product pages
    path('', views.home, name='home'),
    path('products/<str:slug>/', views.products ,name='products'),
    path('products/<str:cat>/<str:slug>/', views.product, name='product'),
    path('lookbook/', views.lookbook, name='lookbook'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),

    # APIS
    path('cart/add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/unauth-cart/', views.unauth_cart, name='unauth_cart'),
    path('cart/updating-cart-total/', views.updating_cart_total, name='updating_cart_total'),
    path('checkout/process-checkout/', views.process_checkout, name='process_checkout'),

    # Policy pages
    path('policy/', views.store_policy, name='store_policy'),
    path('policies/refund-policy/', views.refund_policy, name='refund_policy'),
    path('policies/shipping-information/', views.shipping_policy, name='shipping_policy'),

    # Contact pages
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
