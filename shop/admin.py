from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Product, Customer, Cart, Cart_Item, Review


@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """
    Lists fields for display in admin, fileds for search,
    field filters, fields to prepopulate and rich-text editor.
    """

    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    list_filter = ('status', 'created_on',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content',)


# Register your models here.
myModels = [Customer, Cart, Cart_Item, Review]
admin.site.register(myModels)
