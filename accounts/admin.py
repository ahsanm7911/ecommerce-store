from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Address, Newsletter, Account
# Register your models here.


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_superuser')
    search_fields = ('email', )
    readonly_fields = ('id', 'date_joined', 'last_login')

    ordering = ['email']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register((Address, Newsletter))
admin.site.register(Account, AccountAdmin)

admin.site.site_header = "Unrols Administration"
admin.site.site_title = 'Unrols Admin Panel'
admin.site.index_title = 'Welcome to Unrols Admin Panel'