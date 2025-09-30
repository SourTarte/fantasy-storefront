from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.http import HttpResponseRedirect
from .models import Product


# Create your views here.
class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'product_list.html'


class DebugList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'debug_list.html'


def product_detail(request, product_name, product_id):
    queryset = Product.objects.exclude(stock_quantity=0)
    product = get_object_or_404(queryset, product_name=product_name, id=product_id,)
    reviews = product.reviews.all().order_by("-created_on")
    review_count = product.reviews.all().count()


    return render(
        request,
        "shop/product_page.html",
        {
            "product": product,
            "reviews": reviews,
            "review_count": review_count,
        }
    )