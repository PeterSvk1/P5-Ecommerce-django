from django.test import TestCase
from django.urls import reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.core.exceptions import PermissionDenied


class ErrorHandlerTests(TestCase):

    def test_handler404(self):
        """Test that a 404 error is handled correctly."""

        response = self.client.get('/non-existent-page/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
