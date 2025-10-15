# from django.shortcuts import render, get_object_or_404, redirect
# from django.urls import reverse
from django.views import generic
# from django.contrib import messages
# from django.http import HttpResponseRedirect
from .models import Art
# from .forms import ReviewForm

# ------------------ Product Views ------------------ #


class ArtList(generic.ListView):
    """
    Displays a list of all products.
    """
    queryset = Art.objects.all()
    template_name = 'index.html'