# Importing necessary models and views
from .models import Category, Cart, CartItem
from .views import _cart_id

def counter(request):
    """
    Context processor for counting items in the cart.

    Args:
    request (HttpRequest): The HttpRequest object.

    Returns:
    dict: Dictionary containing 'item_count' which represents the number of items in the cart.
    """
    # Initialize item_count to 0
    item_count = 0

    # Check if the current request is for an admin page
    if 'admin' in request.path:
        # If it's an admin page, return an empty dictionary as admin pages don't need cart item count
        return {}
    else:
        try:
            # Try to retrieve the cart using the _cart_id helper function
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            # Get all cart items for the first cart object
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            # Iterate over each cart item and sum their quantities
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except Cart.DoesNotExist:
            # If the Cart does not exist, set item_count to 0
            item_count = 0

    # Return a dictionary with the total item count
    return dict(item_count=item_count)

def menu_links(request):
    """
    Context processor to provide category links for menu navigation.

    Args:
    request (HttpRequest): The HttpRequest object.

    Returns:
    dict: Dictionary containing 'links' which is a QuerySet of all Category objects.
    """
    # Retrieve all Category objects from the database
    links = Category.objects.all()

    # Return a dictionary containing these category objects
    return dict(links=links)
