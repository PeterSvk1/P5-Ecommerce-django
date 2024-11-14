from django.test import TestCase
from django.urls import reverse
from products.models import Product
from unittest.mock import patch


class BagTests(TestCase):

    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00
        )

    def test_view_bag(self):
        response = self.client.get(reverse('view_bag'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bag/bag.html')


class AddToBagTests(TestCase):

    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00
        )

    def test_add_to_bag_success(self):
        # Add product to the bag
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]), {
                'quantity': 3,
                'redirect_url': reverse('view_bag')
            })

        # Check if the quantity is updated correctly in the session
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 3)

    def test_add_to_bag_maximum_quantity(self):
        # Add more than the maximum allowed quantity
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]), {
                'quantity': 10,
                'redirect_url': reverse('view_bag')
            })

        # Check if the quantity is capped at 5
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 5)

    def test_add_to_bag_error_message(self):
        # Adding more than the max allowed
        response = self.client.post(
            reverse('add_to_bag', args=[self.product.id]), {
                'quantity': 10,
                'redirect_url': reverse('view_bag')
            }, follow=True)

        self.assertContains(response, "max of 5 items")


class AdjustBagTests(TestCase):

    def setUp(self):
        # Create a test product
        self.product = Product.objects.create(
            name='Test Product',
            price=10.00
        )

    def test_adjust_bag_update_quantity(self):
        # Add product to the bag
        self.client.post(reverse('add_to_bag', args=[self.product.id]), {
            'quantity': 2,
            'redirect_url': reverse('view_bag')
        }, follow=True)

        response = self.client.post(
                reverse('adjust_bag', args=[self.product.id]), {
                    'quantity': 4
                }, follow=True)

        # Check if the quantity was updated correctly
        self.assertEqual(self.client.session['bag'][str(self.product.id)], 4)
        self.assertContains(response, "Updated Test Product quantity to 4")

    def test_adjust_bag_remove_item(self):
        # Add product to the bag
        self.client.post(reverse('add_to_bag', args=[self.product.id]), {
            'quantity': 2,
            'redirect_url': reverse('view_bag')
        }, follow=True)

        response = self.client.post(
            reverse('adjust_bag', args=[self.product.id]), {
                'quantity': 0
            }, follow=True)

        # Check if the item was removed
        self.assertNotIn(str(self.product.id), self.client.session['bag'])
        self.assertContains(response, "Removed Test Product from your bag")
