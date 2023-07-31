from django.contrib.sitemaps import Sitemap
from core.models import Product

class ProductsSitemap(Sitemap):
    def items(self):
        return Product.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at