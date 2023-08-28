from django.contrib import admin
from .models import (Product,
                    ProductVariant, 
                    Color,
                    Stock,
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

admin.site.register((ProductVariant, Color, Stock, Cart, CartItem, Order, OrderItem, ShippingAddress ,ConfirmedOrder, ClientEnquiry, CustomerReview))

@admin.register(Product, Category, RefundPolicy, ShippingPolicy)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tiny.js',)

