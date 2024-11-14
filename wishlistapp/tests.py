from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from .models import WishlistItem


class WishlistViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

        # Create a sample product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.99,
            description='A test product for the wishlist',
        )

    def test_add_to_wishlist(self):
        # Test adding a product to the wishlist
        response = self.client.get(
            reverse('add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

        # Check if the wishlist item was created
        wishlist_item_exists = WishlistItem.objects.filter(
            user=self.user, product=self.product
        ).exists()
        self.assertTrue(wishlist_item_exists)

    def test_add_existing_product_to_wishlist(self):
        # Add the product to the wishlist
        WishlistItem.objects.create(user=self.user, product=self.product)

        # Test adding the same product again
        response = self.client.get(
            reverse('add_to_wishlist', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

        wishlist_count = WishlistItem.objects.filter(
            user=self.user, product=self.product).count()
        self.assertEqual(wishlist_count, 1)

    def test_remove_from_wishlist(self):
        # Add a product to the wishlist
        wishlist_item = WishlistItem.objects.create(
            user=self.user, product=self.product)

        # Test removing the product from the wishlist
        response = self.client.get(
            reverse('remove_from_wishlist', args=[wishlist_item.id]))
        self.assertEqual(response.status_code, 302)

        # Check if the wishlist item was removed
        wishlist_item_exists = WishlistItem.objects.filter(
            id=wishlist_item.id
        ).exists()
        self.assertFalse(wishlist_item_exists)
