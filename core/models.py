from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from unrols import settings
from accounts.models import Address
from django.utils.text import slugify
from django.utils import timezone
import uuid
import datetime
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

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, default=' ', blank=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=f'images/primary_images/')
    color = models.TextField(default=' ')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
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
        self.slug = slugify(self.name) # Generating slug from the name
        super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=f'images/other_images/')

    @property
    def get_product_category(self):
       return self.product.category.slug

    def __str__(self):
        return f"Image of {self.product.name}"
    
    

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
    ('Order Confirmed', 'Order Confirmed'),
    ('Shipped to Courier', 'Shipped to Courier'),
    ('Received by Customer', 'Received by Customer'),
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
    status = models.CharField(max_length=30, choices=ORDER_STATUS, default=ORDER_STATUS[0])
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
        return self.transaction_id


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




    






