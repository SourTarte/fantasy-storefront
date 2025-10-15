from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Review, Cart_Item
from .forms import ReviewForm

# ------------------ Product Views ------------------ #


class ProductList(generic.ListView):
    """
    Displays a list of all products.
    """
    queryset = Product.objects.all()
    template_name = 'product_list.html'


class DebugList(generic.ListView):
    """
    Debug view: displays all products for debugging purposes.
    """
    queryset = Product.objects.all()
    template_name = 'debug_list.html'


def product_page(request, product_name, product_id):
    """
    Display a single product's detail page, including reviews and review form.
    Handles review submission via POST.
    """
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(
        queryset,
        product_name=product_name,
        id=product_id)
    reviews = product.reviews.all().order_by("-created_on")
    review_count = product.reviews.all().count()

    # Handle review submission
    if request.method == "POST":
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.username = request.user
            review.product_id = product
            review.save()
            messages.add_message(
                request, messages.SUCCESS,
                'review submitted and awaiting approval'
            )
    # Always provide a fresh review form for GET or after POST
    review_form = ReviewForm()

    return render(
        request,
        "shop/product_page.html",
        {
            "product": product,
            "reviews": reviews,
            "review_count": review_count,
            "review_form": review_form,
        }
    )

# ------------------ Review Views ------------------ #


def review_delete(request, name, product_id, review_id):
    """
    Delete an individual review if the current user is the author.
    Shows a success or error message and redirects to the product page.
    """
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(queryset, name=name, id=product_id)
    review = get_object_or_404(Review, pk=review_id)

    if review.username == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own reviews!')

    return HttpResponseRedirect(
        reverse(
            'product_page',
            args=[
                name,
                product_id]))

# ------------------ Cart Views ------------------ #


def view_cart(request):
    """
    Display the current user's cart with all items and the total price.
    """
    cart_items = Cart_Item.objects.filter(user=request.user)
    total_price = sum(
        item.product.price *
        item.quantity for item in cart_items)
    return render(request, 'shop/cart.html',
                  {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product):
    """
    Add a product to the user's cart, or increment quantity if already present.
    Redirects to the cart view.
    """
    product = Product.objects.get(id=product)
    cart_item, created = Cart_Item.objects.get_or_create(
        product=product, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    """
    Remove a specific item from the user's cart.
    Redirects to the cart view.
    """
    cart_item = Cart_Item.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')


def clear_cart(request):
    """
    Remove all items from the current user's cart.
    Redirects to the cart view.
    """
    cart_items = Cart_Item.objects.filter(user=request.user)
    for item in cart_items:
        item.delete()
    return redirect('view_cart')
