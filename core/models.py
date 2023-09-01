from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.urls import reverse
from unrols import settings
from accounts.models import Address
from django.utils.text import slugify
from django.utils import timezone
from .image_manipulation import resize_and_compress_image
from colorama import Fore
from datetime import datetime, timedelta, date
from PIL import Image
import os
import uuid
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=' ', blank=True)
    description = models.TextField()

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) # Generating slug from name
        super().save(*args, **kwargs)

class Color(models.Model):
    name = models.CharField(max_length=50, default='')
    hex_code = models.CharField(max_length=20, default='')
    image = models.ImageField(upload_to='colors/', default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def slug(self):
        return slugify(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

    def save(self, *args, **kwargs):
        try:
            self.image = resize_and_compress_image(self.image, 100, 85, output=f'{self.slug}-{self.hex_code}')
        except Exception as e:
            print(f'Color image not optimized: {e}', Fore.RED)
        super().save(*args, **kwargs)

class Product(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, default='')
    slug = models.SlugField(unique=True, default=' ', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    lead_time = models.PositiveIntegerField(default=2) # number of days 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.code}'

    def get_absolute_url(self):
        return reverse("product", args=[str(self.category.slug), str(self.slug)])
    
    @property
    def get_category(self):
        return self.category.slug
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) + '-' + slugify(self.code) # Generating slug from the name
        super().save(*args, **kwargs)

def product_variant_image_directory(instance, filename):
    return f'products/{instance.product.slug}/variants/{instance.color.slug}/{filename}'

def product_image_directory(instance, filename):
    return f'products/{instance.product.slug}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_directory, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} | {self.id}'

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    def save(self, *args, **kwargs):
        if not self.pk: # Only on creation, not on update
           super().save(*args, **kwargs)

        try:
            self.image = resize_and_compress_image(self.image, 1080, 85, output=f'{self.product.slug}-{self.id}')
        except Exception as e:
            print('Image not optimized: ', e)



class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    image_original = models.ImageField(upload_to=product_variant_image_directory, default='')
    image_thumbnail = models.ImageField(upload_to=product_variant_image_directory, blank=True)
    image_small = models.ImageField(upload_to=product_variant_image_directory, blank=True)
    image_medium = models.ImageField(upload_to=product_variant_image_directory, blank=True)
    image_large = models.ImageField(upload_to=product_variant_image_directory, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    display = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} - {self.color.name}'
    
    @property
    def product_slug(self):
        return self.product.slug
    
    @property
    def original(self):
        try:
            url = self.image_original.url
        except:
            url = ''
        return url
    
    @property
    def thumbnail(self):
        try:
            url = self.image_thumbnail.url
        except:
            url = ''
        return url
    
    @property
    def small(self):
        try:
            url = self.image_small.url
        except:
            url = ''
        return url

    @property
    def medium(self):
        try:
            url = self.image_medium.url
        except:
            url = ''
        return url

    @property
    def large(self):
        try:
            url = self.image_large.url
        except:
            url = ''
        return url

    def save(self, *args, **kwargs):

        if not self.price:
            self.price = self.product.price
        size = 1600
        self.image_original = resize_and_compress_image(self.image_original, size, 85, output=f'{size}x{size}')
        super().save(*args, **kwargs)
        if self.image_original and not self.image_thumbnail:
            size = 200
            self.image_thumbnail = resize_and_compress_image(self.image_original, size, 100, output=f'{size}x{size}')
            super().save(*args, **kwargs)
        
        if self.image_original and not self.image_small:
            size = 500
            self.image_small = resize_and_compress_image(self.image_original, size, 100, output=f'{size}x{size}')
            super().save(*args, **kwargs)

        if self.image_original and not self.image_medium:
            size = 800
            self.image_medium = resize_and_compress_image(self.image_original, size, 100, output=f'{size}x{size}')
            super().save(*args, **kwargs)

        if self.image_original and not self.image_large:
            size = 1200
            self.image_large = resize_and_compress_image(self.image_original, size, 100, output=f'{size}x{size}')
            super().save(*args, **kwargs)


        if not self.pk: # Only on creation, not on update
           super().save(*args, **kwargs)




class Stock(models.Model):
    variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)   

    def __str__(self):
        return f'{self.variant} - {self.quantity}'

    @property
    def stock(self):
        if self.quantity <= 0:
            return False
        else:
            return True

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    is_complete = models.BooleanField(default=False)

    @property
    def get_order_total(self):
        total = 0
        orderItems = self.orderitem_set.all()
        for item in orderItems:
            total += item.get_item_total
        return total
    
    def __str__(self):
        return f"Order #{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    color = models.CharField(default=' ', max_length=50)

    @property
    def get_item_total(self):
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
    
class CustomPrimaryPrimaryKeyField(models.CharField):
    def get_prep_value(self, value):
        if value is not None:
            # Concatenate the string prefix with the number
            return 'prefix_' + str(value)
        return value

class ShippingAddress(models.Model):
    full_name = models.CharField(max_length=50)
    street = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50, null=True, blank=True, default=' ')
    country = models.CharField(max_length=50, default='Pakistan')
    postal_code = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.full_name} | {self.phone}' 

ORDER_STATUS = [
    ('OC', 'Order Confirmed'),
    ('SC', 'Shipped to Courier'),
    ('RC', 'Received by Customer'),
    ]
CHANNEL = [
    ('WB', 'Website'),
    ('IN', 'Instagram'),
    ('FB', 'Facebook'),
    ('TK', 'Tiktok'),
]

class ConfirmedOrder(models.Model):
    prefix = 'PKUN'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=10, unique=True, editable=False)
    shippingAddress = models.TextField(default=' ')
    order_details = models.TextField(default=' ')
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=40, default='COD')
    status = models.CharField(max_length=255, choices=ORDER_STATUS, default=ORDER_STATUS[0])
    tracking_id = models.CharField(max_length=255, default='', blank=True)
    channel = models.CharField(max_length=255, choices=CHANNEL, default=CHANNEL[0], null=True)
    registered_user = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:

            # Generate the perfixed ID
            last_id = ConfirmedOrder.objects.order_by('-id').first()
            if last_id:
                last_id_number = int(last_id.transaction_id.split(self.prefix)[-1])
                new_id_number = last_id_number + 1
            else:
                new_id_number = 1
            self.transaction_id = f'{self.prefix}{new_id_number:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        split_char = "\n"
        return f"{self.transaction_id} | {self.shippingAddress.split(split_char)[0]}"


class RefundPolicy(models.Model):
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description[:20]
    
class ShippingPolicy(models.Model):
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description[:20]
    
class ClientEnquiry(models.Model):
    name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Client Enquiries'

    def __str__(self):
        return f'{self.email} | {self.comment[:30]}'
    
    
class CustomerReview(models.Model):
    author = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author} | {self.content[:20]}'




    






