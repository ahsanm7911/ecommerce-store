from django.contrib.sitemaps import Sitemap
from core.models import Product
from django.urls import reverse

class MainSitemap(Sitemap):
    def items(self):
        return ['home', 'about', 'contact', 'policy', 'refund_policy', 'shipping_information']
    
    def location(self, item):
        return reverse(item)
    

class ProductsSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at
    