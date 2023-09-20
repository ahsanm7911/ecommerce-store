from django.contrib import admin
from .models import IGPost
# Register your models here.

@admin.register(IGPost)
class IGPostAdmin(admin.ModelAdmin):
    list_display = ('post_url', 'image_tag')
