from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from unrols import settings
from django.dispatch import receiver

# ACCONT CREATION
# create a new user
# create a superuser

class MyAccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Create your models here.
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'
    
def get_default_profile_image():
    return "profile_images/default_profile.png"

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # profile_pic = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    # def get_profile_image_filename(self):
        # return str(self.profile_pic)[str(self.profile_pic).index(f'profile_images/{self.pk}/'):]

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True


class Newsletter(models.Model):
    email = models.CharField(max_length=255)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    street = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def get_full_address(self):
        return f'{self.street}, {self.city}, {self.country}' 
    def __str__(self):
        return self.street
    
@receiver(pre_save, sender=Address)
def ensure_single_set_to_default(sender, instance, **kwargs):
    if instance.is_default:
        # Setting all other objects to False
        sender.objects.exclude(pk=instance.pk).update(is_default=False)




