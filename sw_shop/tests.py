from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress


class UserAuthTests(TestCase):

    def setUp(self):
        # Create a test user with email
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Create an EmailAddress instance for the user and mark it as verified
        email_address = EmailAddress.objects.create(
            user=self.user,
            email=self.user.email,
            verified=True,
            primary=True
        )

        # Set the user as active to bypass the email confirmation flow
        self.user.is_active = True
        self.user.save()

    def test_login_view_with_email(self):
        # Attempt to log in using email
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser@example.com',
            'password': 'testpassword'
        })

        self.assertRedirects(response, reverse('products'))

    def test_login_view_invalid_credentials(self):
        # Test login with invalid credentials
        response = self.client.post(reverse('account_login'), {
            'login': 'testuser@wrong.com',
            'password': 'wrongpassword'
        })

        self.assertFormError(
            response, 'form',
            None,
            'The email address and/or password you specified are not correct.')

    def test_logout_view(self):
        # Log the user in first
        self.client.login(
            email='testuser@example.com', password='testpassword')

        response = self.client.post(reverse('account_logout'))
        self.assertRedirects(response, reverse('home'))

    def test_sign_up_view(self):
        # Test user sign-up
        response = self.client.post(reverse('account_signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })

        self.assertRedirects(
            response, reverse('account_email_verification_sent'))

        self.assertTrue(
            User.objects.filter(email='newuser@example.com').exists())

    def test_sign_up_view_password_common(self):
        # Test sign-up with non-matching passwords
        response = self.client.post(reverse('account_signup'), {
            'username': 'user',
            'password1': 'password123',
            'password2': 'password123',
            'email': 'user@example.com'
        })
        # Check if the form contains the password mismatch error
        self.assertContains(
            response,
            'Your password can’t be a commonly used password.',
            status_code=200)
