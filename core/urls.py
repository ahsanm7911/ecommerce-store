from django.urls import path
from . import views
# urlpatterns here

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<str:slug>/', views.products ,name='products'),
    path('products/<str:cat>/<str:slug>/', views.product, name='product'),
    path('lookbook/', views.lookbook, name='lookbook'),

    # APIS
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('unauth-cart/', views.unauth_cart, name='unauth_cart'),
    path('cart/updating-cart-total/', views.updating_cart_total, name='updating_cart_total'),
    path('checkout/process-checkout/', views.process_checkout, name='process_checkout'),

    path('policies/refund-policy/', views.refund_policy, name='refund_policy'),
    path('policies/shipping-information/', views.shipping_policy, name='shipping_policy'),

    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('policy/', views.store_policy, name='store_policy'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('test/', views.test, name='test'),
]
