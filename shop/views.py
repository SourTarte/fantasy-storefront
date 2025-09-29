from django.views import generic
from .models import Product

# Create your views here.
class ProductList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'product_list.html'

class DebugList(generic.ListView):
    queryset = Product.objects.all()
    template_name = 'debug_list.html'