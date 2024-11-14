from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order
from reviews.models import Review
from wishlistapp.models import WishlistItem
from profiles.models import UserProfile
from products.models import Product
from django.urls import reverse


class UserProfileModelTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

    def test_create_user_profile(self):
        """Test that a UserProfile is created when a User is created."""
        user = self.user
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_user_profile_fields(self):
        """Test that UserProfile fields can be populated."""
        user = self.user
        profile = user.userprofile
        profile.default_phone_number = '1234567890'
        profile.default_country = 'US'
        profile.default_postcode = '12345'
        profile.default_town_or_city = 'Test City'
        profile.default_street_address1 = '123 Test St'
        profile.default_street_address2 = 'Apt 4'
        profile.default_county = 'Test County'

        profile.save()

        profile.refresh_from_db()

        self.assertEqual(profile.default_phone_number, '1234567890')
        self.assertEqual(profile.default_country, 'US')
        self.assertEqual(profile.default_postcode, '12345')
        self.assertEqual(profile.default_town_or_city, 'Test City')
        self.assertEqual(profile.default_street_address1, '123 Test St')
        self.assertEqual(profile.default_street_address2, 'Apt 4')
        self.assertEqual(profile.default_county, 'Test County')


class UserProfileFormTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_user_profile_form_valid(self):
        """Test that a valid form saves the data correctly."""
        profile = self.user.userprofile

        data = {
            'default_phone_number': '1234567890',
            'default_country': 'US',
            'default_postcode': '12345',
            'default_town_or_city': 'Test City',
            'default_street_address1': '123 Test St',
            'default_street_address2': 'Apt 4',
            'default_county': 'Test County',
        }

        form = UserProfileForm(data, instance=profile)
        self.assertTrue(form.is_valid())

        form.save()
        profile.refresh_from_db()

        self.assertEqual(profile.default_phone_number, '1234567890')
        self.assertEqual(profile.default_country, 'US')
        self.assertEqual(profile.default_postcode, '12345')
        self.assertEqual(profile.default_town_or_city, 'Test City')
        self.assertEqual(profile.default_street_address1, '123 Test St')
        self.assertEqual(profile.default_street_address2, 'Apt 4')
        self.assertEqual(profile.default_county, 'Test County')


class UserProfileViewTestCase(TestCase):

    def setUp(self):
        # Create the test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create or get UserProfile
        self.profile, created = UserProfile.objects.get_or_create(
            user=self.user)

        # Create a Product object
        self.product = Product.objects.create(
            name='Test Product',
            description='A test product description',
            price=9.99,
            rating=4.5
        )

        self.wishlist_item = WishlistItem.objects.create(
            user=self.user,
            product=self.product
        )

        # Create an Order for the test user
        self.order = Order.objects.create(
            user_profile=self.profile,
            order_number='12345',
            full_name='Test User',
            email='testuser@example.com',
            phone_number='1234567890',
            country='US',
            postcode='12345',
            town_or_city='Test City',
            street_address1='123 Test St',
            stripe_pid='testpid'
        )

        # Create a Review for the product
        self.review = Review.objects.create(
            user=self.user,
            product=self.product,
            comment='Great product!',
            rating=5
        )

    def test_profile_view(self):
        """Test that the profile view loads
        the correct context and renders the profile."""
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
        self.assertContains(response, 'Great product!')
        self.assertContains(response, '12345')

    def test_order_history_view(self):
        """Test that the order history view loads the correct order details."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, 'Test Product')  # Check for order product
