from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Cart_Item, Wishlist, Wishlist_Item, Review


@admin.action(description="List Items")
def list_items(productadmin, request, queryset):
    queryset.update(status=True)


@admin.action(description="Delist Items")
def delist_items(productadmin, request, queryset):
    queryset.update(status=False)


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = (
        'product_name',
        'price',
        'stock_quantity',
        'category',
        'updated_on',
    )
    search_fields = ['product_name', 'subtitle', 'description',]
    list_filter = ('category', 'updated_on')
    summernote_fields = ('description',)
    actions = [list_items, delist_items]


# Register your models here.
admin.site.register(Review)
admin.site.register(Cart_Item)
admin.site.register(Wishlist)
admin.site.register(Wishlist_Item)
