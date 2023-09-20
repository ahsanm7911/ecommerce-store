from django.db import models
from django.utils.html import mark_safe
from core.image_manipulation import resize_and_compress_image
# Create your models here.

def ig_post_directory(instance, filename):
    return f'ig_media/{instance.id}/{filename}'

class IGPost(models.Model):
    post_url = models.URLField(max_length=255)
    original_image = models.ImageField(upload_to=ig_post_directory, default='')
    medium_image = models.ImageField(upload_to=ig_post_directory, blank=True, null=True, default='')
    thumbnail_image = models.ImageField(upload_to=ig_post_directory, blank=True, null=True, default='')
    display = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # SEO
    alt_tag = models.CharField(max_length=255)

    @property
    def original(self):
        try:
            url = self.original_image.url
        except:
            url = ''
        return url 
    
    @property
    def medium(self):
        try:
            url = self.medium_image.url
        except:
            url = ''
        return url 
    
    @property
    def thumbnail(self):
        try:
            url = self.thumbnail_image.url 
        except:
            url = ''
        return url
    
    def image_tag(self):
        try:
            return mark_safe('<img src="%s" width="100px" height="100px" />' %(self.thumbnail))
        except:
            return mark_safe('<p>No Image.</p>')

    image_tag.short_description =  'Image'

    def __str__(self):
        return self.post_url
    
    def save(self, *args, **kwargs):

        if not self.pk:
            super().save(*args, **kwargs)

        size = 500
        self.medium_image = resize_and_compress_image(self.original_image, size, 70, output=f'{size}x{size}')
        super().save(*args, **kwargs)

        size = 100
        self.thumbnail_image = resize_and_compress_image(self.original_image, size, 100, output=f'{size}x{size}')
        super().save(*args, **kwargs)




