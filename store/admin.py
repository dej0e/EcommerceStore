from django.contrib import admin
from .models import Category, Product, Order, Review

# CategoryAdmin class extends admin.ModelAdmin.
# This class customizes how the Category model is displayed in the Django admin.
class CategoryAdmin(admin.ModelAdmin):
    # list_display is a list of field names to display in the Django admin list view.
    list_display = ['name', 'slug']
    # 'name' and 'slug' are fields from the Category model.

# Registers the Category model with the CategoryAdmin class to the admin site.
# This tells Django: "Use the CategoryAdmin class to represent the Category model in the admin interface."
admin.site.register(Category, CategoryAdmin)

# ProductAdmin class extends admin.ModelAdmin.
# This class customizes the display of the Product model in the Django admin.
class ProductAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin interface.
    list_display = ['name', 'price', 'stock', 'available', 'created', 'updated']
    # Includes essential product details like name, price, stock, and timestamps.

# Registers the Product model with the ProductAdmin class to the admin site.
admin.site.register(Product, ProductAdmin)

# OrderAdmin class for customizing the Order model's display in the admin.
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view of the admin interface for orders.
    list_display = ['id', 'billingName', 'emailAddress', 'created']
    # Shows the order ID, billing name, email address, and creation date.

# Registers the Order model with the OrderAdmin class to the admin site.
admin.site.register(Order, OrderAdmin)

# Review model registration without a custom admin class.
# This will use Django's default options for displaying the Review model in the admin.
admin.site.register(Review)
