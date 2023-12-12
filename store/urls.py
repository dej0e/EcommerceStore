from django.urls import path
from . import views

urlpatterns = [
    # Home page URL pattern.
    # When the root URL ('') is requested, it calls the 'home' view from the views module.
    # 'name' is used to reference this URL pattern in templates and view functions.
    path('', views.home, name='home'),

    # Category-specific page URL pattern.
    # This pattern matches URLs like '/category/books' and calls the 'home' view.
    # 'category_slug' captures the category part of the URL as a slug (a URL-friendly string).
    path('category/<slug:category_slug>', views.home, name='products_by_category'),

    # Product detail page URL pattern.
    # Matches URLs like '/category/books/the-hobbit' and calls the 'productPage' view.
    # Captures 'category_slug' and 'product_slug' to identify the specific product.
    path('category/<slug:category_slug>/<slug:product_slug>',
         views.productPage, name='product_detail'),

    # Add to cart URL pattern.
    # Matches URLs like '/cart/add/5' and calls the 'add_cart' view.
    # Captures the product ID as an integer to identify which product to add to the cart.
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),

    # Cart detail page URL pattern.
    # When '/cart' is requested, it calls the 'cart_detail' view to show the cart contents.
    path('cart', views.cart_detail, name='cart_detail'),

    # Remove item from cart URL pattern.
    # Matches URLs like '/cart/remove/5' and calls the 'cart_remove' view.
    # Captures the product ID to identify which item to remove from the cart.
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),

    # Remove entire product from cart URL pattern.
    # Similar to 'cart_remove', but this removes all quantities of a product from the cart.
    path('cart/remove_product/<int:product_id>', views.cart_remove_product, name='cart_remove_product'),

    # Thank you page URL pattern.
    # Called after a successful order placement. Shows a thank you message with the order ID.
    path('thankyou/<int:order_id>', views.thanks_page, name='thanks_page'),

    # Account creation/signup URL pattern.
    # When '/account/create/' is requested, it calls the 'signupView' for new user registration.
    path('account/create/', views.signupView, name='signup'),

    # Sign-in URL pattern.
    # For user login. Calls the 'signinView' when '/account/signin/' is requested.
    path('account/signin/', views.signinView, name='signin'),

    # Sign-out URL pattern.
    # For user logout. Calls the 'signoutView' when '/account/signout/' is requested.
    path('account/signout/', views.signoutView, name='signout'),

    # Order history URL pattern.
    # Shows the order history for a logged-in user. Calls the 'orderHistory' view.
    path('order_history/', views.orderHistory, name='order_history'),

    # Order detail URL pattern.
    # Shows the details of a specific order. Captures the order ID in the URL.
    path('order/<int:order_id>', views.viewOrder, name='order_detail'),

    # Search functionality URL pattern.
    # Used for searching products. Calls the 'search' view.
    path('search/', views.search, name='search'),
]
