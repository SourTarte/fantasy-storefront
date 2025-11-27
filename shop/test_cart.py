from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product, Cart_Item


class CartViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="alice", password="pass")
        self.client = Client()
        self.client.force_login(self.user)

        # create products with different prices
        self.p_low = Product.objects.create(product_name="Dagger", price=Decimal("5.00"), stock_quantity=2)
        self.p_high = Product.objects.create(product_name="Greatsword", price=Decimal("50.00"), stock_quantity=1)

        # cart items with quantities so line totals differ
        Cart_Item.objects.create(user=self.user, product=self.p_low, quantity=2)   # line_total = 10
        Cart_Item.objects.create(user=self.user, product=self.p_high, quantity=1)  # line_total = 50

    def test_view_cart_returns_sorted_items_and_total(self):
        url = reverse("view_cart")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("cart_items", resp.context)
        cart_items = list(resp.context["cart_items"])

        # server-side view is expected to order by line_total desc (most expensive first)
        line_totals = [item.product.price * item.quantity for item in cart_items]
        self.assertEqual(line_totals, sorted(line_totals, reverse=True))

        # total_price in context should equal sum(product.price * quantity)
        expected_total = sum(item.product.price * item.quantity for item in cart_items)
        self.assertEqual(resp.context.get("total_price"), expected_total)