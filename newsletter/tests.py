from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import mail
from .models import NewsletterSubscription, NewsletterPost
from .forms import NewsletterSubscriptionForm


class NewsletterSubscriptionTests(TestCase):

    def test_subscription_form_valid(self):
        """ Test that the subscription form works
        correctly when a valid email is provided. """
        url = reverse('subscribe')
        data = {'email': 'test@example.com'}
        response = self.client.post(url, data)

        # Check that the form was processed and redirected
        self.assertRedirects(response, reverse('home'))

        self.assertTrue(NewsletterSubscription.objects.filter(
            email='test@example.com').exists())

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject, 'Subscription Confirmation')

    def test_subscription_form_invalid_email_already_subscribed(self):
        """ Test that the form shows an error
        when the user tries to subscribe with an already used email. """

        existing_email = 'test@example.com'
        NewsletterSubscription.objects.create(email=existing_email)

        url = reverse('subscribe')
        data = {'email': existing_email}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse('home'))

        messages_list = list(response.wsgi_request._messages)

        error_message = 'Already subscribed!'

        error_message_found = any(
            message.message == error_message for message in messages_list
        )

        self.assertTrue(error_message_found)

        self.assertEqual(
            NewsletterSubscription.objects.filter(
                email=existing_email).count(), 1)

    def test_newsletter_list_view(self):
        """ Test that newsletters are
        displayed correctly on the newsletter list page. """

        user = User.objects.create_user(
            username='testuser', password='password')

        newsletter = NewsletterPost.objects.create(
            title='Test Newsletter',
            content='This is a test content.',
            author=user
        )

        url = reverse('newsletter_list')
        response = self.client.get(url)

        self.assertContains(response, 'Test Newsletter')
        self.assertContains(response, 'This is a test content.')


class NewsletterPostModelTests(TestCase):

    def test_newsletter_creation(self):
        """ Test that newsletter posts are created successfully. """
        user = User.objects.create_user(
            username='testuser', password='password')
        post = NewsletterPost.objects.create(
            title='Test Newsletter Post',
            content='This is a test content.',
            author=user
        )

        self.assertEqual(post.title, 'Test Newsletter Post')
        self.assertEqual(post.content, 'This is a test content.')
        self.assertEqual(post.author, user)
        self.assertTrue(post.published_date)


class NewsletterSubscriptionFormTests(TestCase):

    def test_subscription_form_valid_data(self):
        """ Test valid subscription form submission. """
        form_data = {'email': 'valid@example.com'}
        form = NewsletterSubscriptionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_subscription_form_invalid_data(self):
        """ Test invalid subscription
        form submission with empty email. """
        form_data = {'email': ''}
        form = NewsletterSubscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_subscription_email_uniqueness(self):
        """ Test that an error is raised
        when the same email is subscribed twice. """
        NewsletterSubscription.objects.create(email='test@example.com')
        form_data = {'email': 'test@example.com'}
        form = NewsletterSubscriptionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
