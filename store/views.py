from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Review
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.template.loader import get_template


from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Category, Product

def home(request, category_slug=None):
    # Initialize variables for category and product list
    category_page = None
    products_list = None

    # Check if category_slug is provided in the URL
    if category_slug is not None:
        # If category_slug is provided, get the corresponding category object
        # If not found, it returns a 404 response
        category_page = get_object_or_404(Category, slug=category_slug)

        # Retrieve all products in the specified category that are marked as available
        products_list = Product.objects.filter(category=category_page, available=True)
    else:
        # If no category_slug is provided, retrieve all available products
        products_list = Product.objects.all().filter(available=True)

    # Paginator is used to divide the list of products into pages
    paginator = Paginator(products_list, 4)  # Show 4 products per page

    try:
        # Try to get the page number from the request GET parameters (querystring)
        page = int(request.GET.get('page', '1'))  # Default to page 1 if not provided
    except ValueError:
        # If the page number in the querystring is not an integer, default to page 1
        page = 1

    try:
        # Get the products for the current page
        products = paginator.page(page)
    except (EmptyPage, InvalidPage):
        # If the page number is invalid (e.g., too high), show the last page
        products = paginator.page(paginator.num_pages)

    # Render and return the response using the 'home.html' template
    # Pass the selected category and products for the current page to the template
    return render(request, 'home.html', {'category': category_page, 'products': products})



def productPage(request, category_slug, product_slug):

    # Try-except block to handle retrieval of a single product based on category and product slugs.
    try:
        # Fetching the product from the database using both the category slug and product slug.
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        # If there is any exception (e.g., Product.DoesNotExist), it is raised further.
        raise e

    # Check if the request is a POST request, the user is authenticated, and the content is not empty.
    if request.method == 'POST' and request.user.is_authenticated and request.POST['content'].strip() != '':
        # Create a new Review object and save it to the database.
        Review.objects.create(
            product=product,  # Associate the review with the found product.
            user=request.user,  # Associate the review with the currently logged-in user.
            content=request.POST['content']  # The content of the review from the POST data.
        )

    # Retrieve all reviews associated with the product.
    reviews = Review.objects.filter(product=product)

    # Render and return the 'product.html' template.
    # The context includes the product object and its associated reviews.
    return render(request, 'product.html', {'product': product, 'reviews': reviews})


def _cart_id(request):

    # Attempt to retrieve the session key (cart ID) from the current session.
    cart = request.session.session_key

    # Check if the cart variable is empty, indicating that there is no session key.
    if not cart:
        # Since there is no session key, create a new session.
        # This will generate a new session key.
        cart = request.session.create()

    # Return the session key (cart ID), which is either retrieved or newly created.
    return cart


def add_cart(request, product_id):

    # Retrieve the product from the database based on the provided product ID.
    product = Product.objects.get(id=product_id)

    try:
        # Attempt to retrieve the cart using the current session's cart ID.
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        # If the cart does not exist, create a new cart with the current session's cart ID.
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        # Attempt to retrieve the cart item for the current product and cart.
        cart_item = CartItem.objects.get(product=product, cart=cart)

        # Check if adding another product does not exceed the stock.
        if cart_item.quantity < cart_item.product.stock:
            # Increment the quantity of the product in the cart.
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the cart item does not exist, create a new cart item with the product, a quantity of 1, and the cart.
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    # Redirect to the 'cart_detail' view after adding the product to the cart.
    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):

    try:
        # Retrieve the cart using the session's cart ID.
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # Fetch all active items in the cart.
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        # Calculate the total price and item count in the cart.
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        # If the cart does not exist, do nothing (cart remains empty).
        pass

    # Setting Stripe's secret key for payment processing.
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # Converting the total amount to cents for Stripe processing.
    stripe_total = int(total * 100)
    # Description for the Stripe charge.
    description = 'Z-Store - New Order'
    # Stripe publishable key for the frontend.
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    # Check if the request is a POST request, indicating a form submission for payment.
    if request.method == 'POST':
        try:
            # Retrieving Stripe token and billing/shipping details from the form.
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']

            # Creating Stripe customer and charge.
            customer = stripe.Customer.create(email=email, source=token)
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )

            try:
                # Creating an order in the database.
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )

                # Creating order items and updating stock.
                for order_item in cart_items:
                    OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details
                    )

                    # Reduce the stock of the ordered product.
                    product = Product.objects.get(id=order_item.product.id)
                    product.stock = int(product.stock - order_item.quantity)
                    product.save()

                    # Deleting the item from the cart after adding to the order.
                    order_item.delete()

                # Redirect to the thank you page after successful order placement.
                return redirect('thanks_page', order_details.id)
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            # Handling Stripe card error.
            return False, e

    # Rendering the 'cart.html' template with the cart details.
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'counter': counter,
        'data_key': data_key,
        'stripe_total': stripe_total,
        'description': description
    })

def cart_remove(request, product_id):

    # Retrieve the cart using the session's cart ID.
    cart = Cart.objects.get(cart_id=_cart_id(request))

    # Fetch the product based on the provided product ID or return a 404 error if not found.
    product = get_object_or_404(Product, id=product_id)

    # Retrieve the specific cart item for the given product in the user's cart.
    cart_item = CartItem.objects.get(product=product, cart=cart)

    # Check if the cart item's quantity is greater than one.
    if cart_item.quantity > 1:
        # If so, decrease the quantity by one.
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # If the quantity is one, remove the cart item entirely.
        cart_item.delete()

    # After modifying the cart, redirect the user to the cart detail page.
    return redirect('cart_detail')


def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


def thanks_page(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)
    return render(request, 'thankyou.html', {'customer_order': customer_order})


def signupView(request):

    # Check if the current request is a POST request, indicating form submission.
    if request.method == 'POST':
        # Create an instance of the SignUpForm with the submitted data.
        form = SignUpForm(request.POST)

        # Validate the form.
        if form.is_valid():
            # Save the new user to the database.
            form.save()

            # Retrieve the username from the form's cleaned data.
            username = form.cleaned_data.get('username')

            # Fetch the newly created user instance from the database.
            signup_user = User.objects.get(username=username)

            # Retrieve the 'Customer' group.
            customer_group = Group.objects.get(name='Customer')

            # Add the new user to the 'Customer' group.
            customer_group.user_set.add(signup_user)

            # Log the user in (create a session for the new user).
            login(request, signup_user)

            # Optionally, you can redirect the user to a different page after successful registration.
            # For example: return redirect('home')

    # If the request is not a POST request, create a new instance of SignUpForm to display the form.
    else:
        form = SignUpForm()

    # Render and return the 'signup.html' template with the SignUpForm instance.
    return render(request, 'signup.html', {'form': form})


def signinView(request):

    # Check if the current request is a POST request, which indicates form submission.
    if request.method == 'POST':
        # Create an instance of the AuthenticationForm with the submitted data.
        form = AuthenticationForm(data=request.POST)

        # Validate the form.
        if form.is_valid():
            # Retrieve the username and password from the form submission.
            username = request.POST['username']
            password = request.POST['password']

            # Authenticate the user. This checks if the credentials are valid.
            user = authenticate(username=username, password=password)

            # Check if the authentication was successful (i.e., if the user object is not None).
            if user is not None:
                # Log the user in (create a user session).
                login(request, user)

                # Redirect the user to the home page after successful login.
                return redirect('home')
            else:
                # If authentication failed, redirect to the sign-up page.
                # This line can be modified to redirect to a different page or show an error message instead.
                return redirect('signup')

    # If the request is not a POST request, create a new instance of AuthenticationForm to display the form.
    else:
        form = AuthenticationForm()

    # Render and return the 'signin.html' template with the AuthenticationForm instance.
    return render(request, 'signin.html', {'form': form})


def signoutView(request):
    logout(request)
    return redirect('signin')


@login_required(redirect_field_name='next', login_url='signin')
def orderHistory(request):

    # Check if the current user is authenticated. This is technically redundant due to
    # the @login_required decorator but serves as an additional layer of verification.
    if request.user.is_authenticated:
        # Retrieve the user's email address.
        email = str(request.user.email)

        # Query the Order model for orders that match the user's email address.
        order_details = Order.objects.filter(emailAddress=email)

        # Printing the email and order details to the console (useful for debugging purposes).
        print(email)
        print(order_details)

    # Render and return the 'orders_list.html' template.
    # Pass the retrieved order details to the template.
    return render(request, 'orders_list.html', {'order_details': order_details})


@login_required(redirect_field_name='next', login_url='signin')
def viewOrder(request, order_id):

    # Check if the current user is authenticated. This check is technically redundant due to
    # the @login_required decorator but acts as an additional layer of verification.
    if request.user.is_authenticated:
        # Retrieve the user's email address.
        email = str(request.user.email)

        # Fetch the specific order by its ID and the user's email address. This ensures that
        # users can only access their own orders.
        order = Order.objects.get(id=order_id, emailAddress=email)

        # Retrieve all items associated with the order.
        order_items = OrderItem.objects.filter(order=order)

    # Render and return the 'order_detail.html' template.
    # Pass the order and its associated items to the template for display.
    return render(request, 'order_detail.html', {'order': order, 'order_items': order_items})

def search(request):

    # Retrieve the search query from the request's GET parameters.
    search_query = request.GET.get('title', '')

    # Filter the Product objects based on the search query.
    products = Product.objects.filter(name__icontains=search_query)

    # Render and return the 'home.html' template.
    return render(request, 'home.html', {'products': products})
