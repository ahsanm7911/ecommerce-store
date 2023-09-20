from django.contrib import admin
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import (Product,
                    ProductVariant, 
                    ProductImage,
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
                    CustomerReview, 
                    About,
                    FAQ)
# Register your models here.

admin.site.register((ProductImage, Color, Cart, CartItem, Order, OrderItem, ShippingAddress ,ConfirmedOrder, ClientEnquiry, CustomerReview))

@admin.register(Category, RefundPolicy, ShippingPolicy, About, FAQ)
class PostAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/tiny.js',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image_tag', 'view_variants_link',)
    fields = ('category', 'name', 'code', 'slug', 'description', 'old_price', 'price', 'lead_time', 'title_tag', 'meta_description', 'keywords')
    list_filter = ('category', )
    search_fields = ('name__icontains', 'code__icontains')

    class Media:
        js = ('js/tiny.js', )

    def view_variants_link(self, obj):
        count = obj.productvariant_set.all().count()
        url = (
            reverse("admin:core_productvariant_changelist")
            + "?"
            + urlencode({"product__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Variants</a>', url, count)
    
    view_variants_link.short_description = "Variants"

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'image_tag','stock_link',)
    search_fields = ('price__startswith',)
    list_filter = ('price', 'created_at')

    def stock_link(self, obj):
        stock = obj.get_stock()
        url = f'/admin/core/stock/{obj.stock.id}/change/'
        if stock < 2 and stock > 0:
            html_content = '<a href="{}">{} Items <span style="color:orange;">&nbsp;Low!</span></a>'
        elif stock >= 2:
            html_content = '<a href="{}">{} Items <span style="color:green;">&nbsp;Ok!</span></a>'
        elif stock == 0:
            html_content = '<a href="{}">{} Items <span style="color:red;">&nbsp;Empty!</span></a>'
        return format_html(html_content, url, stock)
    
    stock_link.short_description = "Stock"
    
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('variant', 'quantity', 'image_tag')

