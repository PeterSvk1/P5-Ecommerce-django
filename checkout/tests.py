from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch
from products.models import Product
from .models import Order, OrderLineItem
from bag.views import view_bag
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.core import mail


class CheckoutTests2(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(
            username='testuser', password='testpassword')

    @patch('stripe.PaymentIntent.modify')
    def test_cache_checkout_data(self, mock_modify):

        response = self.client.post(
            reverse('cache_checkout_data'), data={
                'client_secret': 'test_client_secret_123',
                'save_info': 'on',
            })
        # Check if stripe.PaymentIntent.modify was called with the correct data
        mock_modify.assert_called_with(
            'test_client',
            metadata={'bag': '{}', 'save_info': 'on', 'username': self.user}
        )
        self.assertEqual(response.status_code, 200)

    @patch('stripe.PaymentIntent.confirm')
    def test_payment_success(self, mock_confirm):
        # Simulate a successful payment
        mock_confirm.return_value = {'status': 'succeeded'}

        # Create an order
        order = Order.objects.create(
            full_name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            stripe_pid="stripe_pid_test"
        )

        response = self.client.get(
            reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)
        order = Order.objects.get(order_number=order.order_number)
        self.assertEqual(order.stripe_pid, 'stripe_pid_test')
        self.assertEqual(order.full_name, 'Test User')

    @patch('stripe.PaymentIntent.confirm')
    def test_payment_failure(self, mock_confirm):
        # Simulate a failed payment
        mock_confirm.return_value = {'status': 'failed'}

        order = Order.objects.create(
            full_name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            stripe_pid="stripe_pid_test"
        )

        response = self.client.post(
            reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)

        order = Order.objects.get(
            order_number=order.order_number)

        self.assertEqual(order.stripe_pid, 'stripe_pid_test')
        self.assertEqual(order.full_name, 'Test User')

    def test_success_message(self):
        order = Order.objects.create(
            full_name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            stripe_pid="stripe_pid_test"
        )

        response = self.client.get(
            reverse('checkout_success', args=[order.order_number]))
        self.assertContains(response, "Thank you")


class EmailTests(TestCase):

    def test_confirmation_email_sent(self):
        """
        Test that a confirmation email is sent after successful checkout
        """
        # Set up the order (you can reuse the order creation test)
        order = Order.objects.create(
            full_name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            stripe_pid="stripe_pid_test",
        )

        response = self.client.get(
            reverse('checkout_success', args=[order.order_number]))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        expected_subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        ).strip()

        self.assertEqual(email.subject, expected_subject)
        self.assertIn("Thank you for your order", email.body)


class OrderTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product", price=10)
        self.user = User.objects.create_user(
            username="testuser", password="password")
        self.client.login(
            username="testuser", password="password")

    def test_order_creation(self):
        # Simulate checkout by creating an order manually
        order = Order.objects.create(
            order_number=self.user,
            full_name="Test User",
            email="testuser@example.com",
            phone_number="1234567890",
            country="US",
            postcode="12345",
            town_or_city="Test City",
            street_address1="123 Test St",
            stripe_pid="stripe_pid_test"
        )
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.order_number, self.user)
        self.assertEqual(order.full_name, "Test User")


class OrderLineItemSignalTests(TestCase):

    def setUp(self):
        # Create a test order and product
        self.order = Order.objects.create(
            full_name='Test User',
            email='test@example.com',
            phone_number='1234567890',
            country='Testland',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test Street',
            street_address2='',
            county='Test County'
        )

        self.product = Product.objects.create(
            name='Test Product',
            price=10.00,
            description='A test product'
        )
