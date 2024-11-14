from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from .models import Review, ContactMessage
from django.contrib.messages import get_messages
from django.core import mail


class ReviewViewsTestCase(TestCase):

    def setUp(self):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                'admin', 'lineage4ever88@gmail.com', 'password')

        self.user = User.objects.create_user(
            username='reviewuser', password='reviewpassword')
        self.client = Client()

        self.product = Product.objects.create(
            name='Sample Product',
            price=15.99,
            description='A sample product for testing reviews',
        )

    def test_submit_review_logged_in(self):

        self.client.login(username='reviewuser', password='reviewpassword')

        # Test submitting a valid review
        response = self.client.post(
            reverse('submit_review', args=[self.product.id]), {
                'comment': 'This is a test review.',
                'rating': 4.5
            })
        self.assertEqual(response.status_code, 302)

        # Check if the review was created
        review_exists = Review.objects.filter(
            user=self.user,
            product=self.product, comment='This is a test review.'
        ).exists()
        self.assertTrue(review_exists)

    def test_submit_review_not_logged_in(self):
        self.client.logout()

        response = self.client.post(
            reverse('submit_review', args=[self.product.id]), {
                'comment': 'Attempted review without login.',
                'rating': 4.0
            })

        self.assertRedirects(
            response,
            f'{reverse("account_login")}?next={
                reverse("submit_review", args=[self.product.id])}'
        )

    def test_reviews_list_view(self):
        # Create a review for the product
        Review.objects.create(
            product=self.product,
            user=self.user,
            comment='Another test review.',
            rating=3.0
        )

        response = self.client.get(reverse('reviews_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another test review.')

    def test_contact_form_submission(self):
        # Define test data
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'message': 'This is a test message.'
        }

        response = self.client.post(reverse('contact'), data)

        self.assertEqual(ContactMessage.objects.count(), 1)
        contact_message = ContactMessage.objects.first()
        self.assertEqual(contact_message.name, 'Test User')
        self.assertEqual(contact_message.email, 'testuser@example.com')
        self.assertEqual(contact_message.message, 'This is a test message.')

        self.assertRedirects(response, reverse('contact'))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your message has been sent!')

        admin_email = User.objects.get(username='admin').email
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, [admin_email])
        self.assertEqual(mail.outbox[1].to, ['testuser@example.com'])

    def test_contact_form_invalid(self):
        # Make a POST request with invalid data
        data = {
            'name': 'Test User',
            'email': 'testuser@example.com',
            'message': ''
        }

        response = self.client.post(reverse('contact'), data)

        # Check that no ContactMessage was created
        self.assertEqual(ContactMessage.objects.count(), 0)

        # Check if the page returns with errors
        self.assertFormError(
            response, 'form', 'message', 'This field is required.')


class ReviewDeleteTestCase(TestCase):
    def setUp(self):
        """Create a test product and user to simulate review deletion."""
        self.product = Product.objects.create(
            name="Test Product", price=100.00, description="A test product.")
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.review = Review.objects.create(
            product=self.product,
            user=self.user,
            comment="Great product!",
            rating=4.5
        )

    def test_review_deletion(self):
        """Test that a review can be
        deleted and the user is redirected to their profile page."""

        self.assertEqual(Review.objects.count(), 1)

        self.client.login(username='testuser', password='testpassword')

        delete_url = reverse('delete_review', args=[self.review.id])

        response = self.client.post(delete_url)

        self.assertEqual(Review.objects.count(), 0)

        self.assertRedirects(response, reverse('profile'))
