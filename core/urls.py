from django.urls import path
from . import views
from accounts import views as account_views
# urlpatterns here

urlpatterns = [

    # SEO
    path('test/', views.test, name='test'),
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
    path('shipping-and-returns/', views.shipping_and_returns, name='shipping-and-returns'),
    path('terms-and-conditions/', views.terms_and_conditions, name='terms-and-conditions'),

    # Contact pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs')
]
