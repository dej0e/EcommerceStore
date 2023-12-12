from django.contrib import admin
from .models import Category, Product, Order, Review

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Category, CategoryAdmin)

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']

admin.site.register(Product, ProductAdmin)

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'billingName', 'emailAddress', 'created']

admin.site.register(Order, OrderAdmin)

# Review Model
admin.site.register(Review)
