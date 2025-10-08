from django import forms
from .models import Review, Cart_Item
from crispy_forms.helper import FormHelper



class ReviewForm(forms.ModelForm):
    """
    Form class for users to comment on a post 
    """
    
    class Meta:
        """
        Specify the django model and order of the fields
        """
        model = Review
        fields = ['title', 'content', 'review_score',]