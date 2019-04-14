from django.contrib.admin import AdminSite, ModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from solo.admin import SingletonModelAdmin

from ..models import PlatformVersion, PriceVariable, Category, Product, ProductPriceTier, ProductScreenshot, ProductVersion, Vendor, SiteConfiguration, Server, \
    Account, License, User


class PlumAdminSite(AdminSite):
    site_header = 'plum'


class PriceTierInline(TabularInline):
    model = ProductPriceTier
    extra = 0


class ScreenshotInline(TabularInline):
    model = ProductScreenshot
    extra = 0


class VersionInline(StackedInline):
    model = ProductVersion
    extra = 0


class ProductAdmin(ModelAdmin):
    inlines = [
        VersionInline,
        PriceTierInline,
        ScreenshotInline,
    ]
    list_display = ['name', 'category', 'is_paid', 'approved', 'certified', 'stability']


class VersionAdmin(ModelAdmin):
    list_display = ['name', 'release_date']
    search_fields = ['release_date']


class VendorAdmin(ModelAdmin):
    list_display = ['name', 'certified']


class ServerInline(TabularInline):
    model = Server
    extra = 0


class AccountAdmin(ModelAdmin):
    inlines = [ServerInline]


class LicenseAdmin(ModelAdmin):
    list_display = ['id', 'account', 'product', 'start_date', 'end_date']
    list_filter = ['product', 'start_date', 'end_date']
    search_fields = ['product__name', 'account__name']


class CustomUserAdmin(UserAdmin):
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('first_name', 'last_name', 'email')


site = PlumAdminSite(name='admin')
site.register(PlatformVersion, VersionAdmin)
site.register(PriceVariable)
site.register(Category)
site.register(Vendor, VendorAdmin)
site.register(Product, ProductAdmin)
site.register(SiteConfiguration, SingletonModelAdmin)
site.register(Account, AccountAdmin)
site.register(License, LicenseAdmin)
site.register(User, CustomUserAdmin)
