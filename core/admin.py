from django.contrib import admin
from .models import (Product,
                    ProductImage, 
                    Cart, 
                    CartItem, 
                    Order, 
                    OrderItem, 
                    Category, 
                    ShippingAddress, 
                    ConfirmedOrder, 
                    RefundPolicy, 
                    ShippingPolicy, 
                    ClientEnquiry,
                    CustomerReview)
# Register your models here.

admin.site.register((ProductImage, Cart, CartItem, Order, OrderItem, ShippingAddress ,ConfirmedOrder, ClientEnquiry, CustomerReview))

@admin.register(Product, Category, RefundPolicy, ShippingPolicy)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tiny.js',)

