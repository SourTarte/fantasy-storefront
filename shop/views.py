from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import F, ExpressionWrapper, DecimalField
from .models import Product, Review, Cart_Item, Wishlist, Wishlist_Item
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


def review_delete(request, product_name, product_id, review_id):
    """
    Delete an individual review if the current user is the author.
    Shows a success or error message and redirects to the product page.
    """
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(queryset, product_name=product_name, id=product_id)
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
                product_name,
                product_id]))


# ---------------- Wishlist Views ---------------- #


def view_wishlist(request):
    """
    Display the current user's wishlist, with items sorted by line cost
    (product.price * wishlist_item.quantity).
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    # Annotate each wishlist item with a computed line_total and sort by it descending
    wishlist_items = Wishlist_Item.objects.filter(wishlist=wishlist).annotate(
        line_total=ExpressionWrapper(
            F('product__price') * F('quantity'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    ).order_by('-line_total')

    return render(request, 'shop/wishlist.html', {
        'wishlist_items': wishlist_items,
        'wishlist': wishlist,
    })

def add_to_wishlist(request, product):
    """
    Add a product to the user's wishlist. For normal requests redirect to view_wishlist.
    For AJAX requests return JSON so the frontend can show a modal without redirect.
    """
    product = get_object_or_404(Product, id=product)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist_item, created = Wishlist_Item.objects.get_or_create(
        product=product, wishlist=wishlist)
    # ensure saved (get_or_create already saved when created)
    wishlist_item.save()

    # Return JSON for AJAX requests (fetch/XHR)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": "ok", "message": "Saved To Wishlist"})

    # Fallback for non-AJAX requests (preserve existing behaviour)
    return redirect("view_wishlist")


def remove_from_wishlist(request, item_id):
    """
    Remove a specific item from the user's cart.
    Redirects to the cart view.
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    queryset = Wishlist_Item.objects.filter(wishlist=wishlist)
    wishlist_item = get_object_or_404(queryset, id=item_id)
    wishlist_item.delete()
    return redirect('view_wishlist')


def save_cart_to_wishlist(request):
    """
    Remove all items from the current user's cart, and adds them to the user's wishlist.
    Redirects to the cart view.
    """
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    cart_items = Cart_Item.objects.filter(user=request.user)
    for item in cart_items:
        wishlist_item, created = Wishlist_Item.objects.get_or_create(
        product=item.product, wishlist=wishlist)
        # ensure saved (get_or_create already saved when created)
        wishlist_item.save()
        item.delete()
    return redirect('view_wishlist')


# ------------------ Cart Views ------------------ #


def view_cart(request):
    """
    Display the current user's cart, with items sorted by line cost
    (product.price * cart_item.quantity).
    """
    cart_items = Cart_Item.objects.filter(user=request.user).annotate(
        line_total=ExpressionWrapper(
            F('product__price') * F('quantity'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    ).order_by('-line_total')

    # total_price computed as before
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


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


@require_POST
def increment_in_cart(request, cart_item_id, add_subtract):
    """
    Adjust Cart_Item.quantity by +1 (add_subtract=1) or -1 (add_subtract=0).
    If quantity would become <= 0, remove the Cart_Item.
    Only modifies items owned by the current user.
    """
    # Ensure we only touch items belonging to the logged-in user
    cart_item = get_object_or_404(Cart_Item, id=cart_item_id, user=request.user)

    # Normalize add_subtract to int and apply change
    if int(add_subtract) == 0:
        cart_item.quantity = max(0, cart_item.quantity - 1)
    else:
        cart_item.quantity += 1

    # If quantity is zero or less, delete the item; otherwise save the new quantity
    if cart_item.quantity <= 0:
        cart_item.delete()
        messages.add_message(request, messages.SUCCESS, "Item removed from cart")
    else:
        cart_item.save()
        messages.add_message(request, messages.SUCCESS, "Cart updated")

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
