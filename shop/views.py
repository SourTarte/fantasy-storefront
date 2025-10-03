from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Product, Review
from .forms import ReviewForm


# Create your views here.
class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'product_list.html'


class DebugList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'debug_list.html'


def product_page(request, product_name, product_id):
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(queryset, product_name=product_name, id=product_id,)
    reviews = product.reviews.all().order_by("-created_on")
    review_count = product.reviews.all().count()
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

def review_delete(request, product_name, product_id, review_id):
    """
    Delete an individual review.

    **Context**

    ``product``
        An instance of :model:`shop.Product`.
    ``review``
        A single review related to the product.
    """
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(queryset, product_name=product_name, id=product_id,)
    review = get_object_or_404(Review, pk=review_id)

    if review.username == request.user:
        review.delete()
        messages.add_message(request, messages.SUCCESS, 'Review deleted!')
    else:
        messages.add_message(request, messages.ERROR,
                             'You can only delete your own reviews!')
        
    return HttpResponseRedirect(reverse('product_page', args=[product_name, product_id]))