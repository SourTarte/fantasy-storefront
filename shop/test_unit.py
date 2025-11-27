from decimal import Decimal
from django.test import TestCase
from django.contrib import admin as django_admin
from django.db import models
from .test_admin import list_items, delist_items, ProductAdmin
from .models import Product, Review, Cart_Item, Wishlist, Wishlist_Item

# language: python

# relative imports of the objects to test (admin actions and admin class)


class AdminRegistrationAndActionsTests(TestCase):
    """
    Tests for admin registrations, ProductAdmin configuration,
    and the list/delist admin actions.
    """

    def test_models_registered_in_admin(self):
        # admin.site._registry maps models to ModelAdmin instances
        reg = django_admin.site._registry
        self.assertIn(Product, reg, "Product should be registered in admin")
        self.assertIn(Review, reg, "Review should be registered in admin")
        self.assertIn(Cart_Item, reg, "Cart_Item should be registered in admin")
        self.assertIn(Wishlist, reg, "Wishlist should be registered in admin")
        self.assertIn(Wishlist_Item, reg, "Wishlist_Item should be registered in admin")

    def test_productadmin_configuration(self):
        reg = django_admin.site._registry
        # get the ModelAdmin instance registered for Product
        product_admin_instance = reg.get(Product)
        self.assertIsNotNone(product_admin_instance, "Product model must have a ModelAdmin instance registered")

        # Check that the registered admin is an instance of the declared ProductAdmin class
        self.assertIsInstance(product_admin_instance, ProductAdmin, "Registered Product admin should be an instance of ProductAdmin")

        # Validate configured display/search/filter/summernote fields
        expected_list_display = ('product_name', 'price', 'stock_quantity', 'category', 'updated_on')
        self.assertEqual(tuple(product_admin_instance.list_display), expected_list_display)

        # search_fields should include these entries
        for field in ['product_name', 'subtitle', 'description']:
            self.assertIn(field, getattr(product_admin_instance, 'search_fields', []))

        # list_filter should contain category and updated_on
        for f in ('category', 'updated_on'):
            self.assertIn(f, getattr(product_admin_instance, 'list_filter', ()))

        # summernote_fields should include 'description'
        self.assertIn('description', getattr(product_admin_instance, 'summernote_fields', ()))

        # actions should include our admin action callables
        actions = getattr(product_admin_instance, 'actions', [])
        self.assertIn(list_items, actions, "list_items action must be attached to ProductAdmin actions")
        self.assertIn(delist_items, actions, "delist_items action must be attached to ProductAdmin actions")

    def test_action_descriptions_present(self):
        # The @admin.action decorator provides a description attribute (Django 3.2+)
        desc_list = getattr(list_items, 'description', None) or getattr(list_items, 'short_description', None)
        desc_delist = getattr(delist_items, 'description', None) or getattr(delist_items, 'short_description', None)
        self.assertEqual(desc_list, "List Items")
        self.assertEqual(desc_delist, "Delist Items")

    def test_list_and_delist_actions_update_status(self):
        # Create products with default status False
        p1 = Product.objects.create(
            product_name="Sword of Testing",
            price=Decimal('15.00'),
            stock_quantity=3,
            description="A test sword."
        )
        p2 = Product.objects.create(
            product_name="Shield of Assertions",
            price=Decimal('20.00'),
            stock_quantity=2,
            description="A test shield."
        )

        # Ensure initial status is False (unlisted) for clarity
        Product.objects.filter(id__in=[p1.id, p2.id]).update(status=False)

        qs = Product.objects.filter(id__in=[p1.id, p2.id])

        # Apply list_items action; it should set status=True for selected queryset
        list_items(None, None, qs)
        # Refresh from DB and assert
        p1.refresh_from_db()
        p2.refresh_from_db()
        self.assertTrue(p1.status, "After list_items action, product 1 should be listed")
        self.assertTrue(p2.status, "After list_items action, product 2 should be listed")

        # Apply delist_items action; it should set status=False
        delist_items(None, None, qs)
        p1.refresh_from_db()
        p2.refresh_from_db()
        self.assertFalse(p1.status, "After delist_items action, product 1 should be unlisted")
        self.assertFalse(p2.status, "After delist_items action, product 2 should be unlisted")