from django.test import TestCase
from .forms import ReviewForm


class TestCommentForm(TestCase):

    def test_form_is_valid(self):
        review_form = ReviewForm({
            'product_id': '1',
            'username': 'User1',
            'title': 'Wow what a good product',
            'content': 'This is a great product',
            'review_score': '3'
            })
        self.assertTrue(review_form.is_valid())