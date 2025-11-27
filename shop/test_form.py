from django.test import TestCase
from shop.forms import ReviewForm


class ReviewFormTest(TestCase):
    def test_review_form_valid_with_expected_fields(self):
        # adjust keys to match your ReviewForm fields (title/content/review_score/etc.)
        data = {
            "title": "Solid blade",
            "content": "Cuts very well, 10/10.",
            "review_score": 5,
        }
        form = ReviewForm(data=data)
        self.assertTrue(form.is_valid(), msg=f"Form errors: {form.errors}")