from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    # Fields for category details
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)  # Used in URLs
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)  # Default ordering by category name
        verbose_name = 'category'  # Singular form in admin panel
        verbose_name_plural = 'categories'  # Plural form in admin panel

    def get_url(self):
        # Returns the URL for a category. Used in templates for linking to a category page.
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        # String representation of a Category object. Used in admin panels and debug prints.
        return self.name

class Product(models.Model):
    # Fields for product details
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)  # Used in URLs
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to Category
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)  # Whether the product is available for sale
    created = models.DateTimeField(auto_now_add=True)  # Automatically set when object is created
    updated = models.DateTimeField(auto_now=True)  # Automatically set on each save

    class Meta:
        ordering = ('name',)  # Default ordering by product name
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        # Returns the URL for a product. Used in templates for linking to a product page.
        return reverse('product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        # String representation of a Product object.
        return self.name

class Cart(models.Model):
    # Unique identifier for the cart
    cart_id = models.CharField(max_length=250, blank=True)
    # Date when the cart was created, set automatically
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'  # Custom database table name
        ordering = ['date_added']  # Default ordering by the date added

    def __str__(self):
        # String representation showing the cart's ID
        return self.cart_id

class CartItem(models.Model):
    # Foreign key relation to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Foreign key relation to the Cart model
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()  # Quantity of the product in the cart
    active = models.BooleanField(default=True)  # Status of the cart item

    class Meta:
        db_table = 'CartItem'  # Custom database table name

    def sub_total(self):
        # Calculate the subtotal for this cart item
        return self.product.price * self.quantity

    def __str__(self):
        # String representation showing the related product's name
        return str(self.product)

class Order(models.Model):
    # Unique token for the order
    token = models.CharField(max_length=250, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
    # Email address for the order
    emailAddress = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
    # Date and time when the order was created or updated, set automatically
    created = models.DateTimeField(auto_now=True)
    # Billing details
    billingName = models.CharField(max_length=250, blank=True)
    billingAddress1 = models.CharField(max_length=250, blank=True)
    billingCity = models.CharField(max_length=250, blank=True)
    billingPostcode = models.CharField(max_length=250, blank=True)
    billingCountry = models.CharField(max_length=250, blank=True)
    # Shipping details
    shippingName = models.CharField(max_length=250, blank=True)
    shippingAddress1 = models.CharField(max_length=250, blank=True)
    shippingCity = models.CharField(max_length=250, blank=True)
    shippingPostcode = models.CharField(max_length=250, blank=True)
    shippingCountry = models.CharField(max_length=250, blank=True)

    class Meta:
        db_table = 'Order'  # Custom database table name
        ordering = ['-created']  # Default ordering by creation date, newest first

    def __str__(self):
        # String representation showing the order's ID
        return str(self.id)

class OrderItem(models.Model):
    # Product name for the order item
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()  # Quantity of the product in the order
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
    # Foreign key relation to the Order model
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        db_table = 'OrderItem'  # Custom database table name

    def sub_total(self):
        # Calculate the subtotal for this order item
        return self.quantity * self.price

    def __str__(self):
        # String representation showing the related product's name
        return self.product

class Review(models.Model):
    # Foreign key relation to the Product model
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # Foreign key relation to the User model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)  # Content of the review

    def __str__(self):
        # String representation showing the review's content
        return self.content
