from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Customer, Cart, Cart_Item, Review


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """
    list_display = ('product_name', 'price', 'stock_quantity', 'category',)
    search_fields = ['product_name', 'description']
    list_filter = ('stock_quantity', 'price',)
    summernote_fields = ('description',)


# Register your models here.
myModels = [Customer, Cart, Cart_Item, Review]
admin.site.register(myModels)
