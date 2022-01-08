from django.contrib import admin
from .models import Product, ProductLink, ProductAttribute, ProductImages


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 3


class ProductImageInline(admin.TabularInline):
    model = ProductImages


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    list_filter = ('created', )
    search_fields = ('title', 'description')
    inlines = (ProductAttributeInline, ProductImageInline)


@admin.register(ProductLink)
class ProductLinkInline(admin.ModelAdmin):
    list_display = ('url', 'flag')
    list_filter = ('flag', )
