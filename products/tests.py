from django.test import TestCase
from .models import Product, Category
from reviews.models import Review
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.messages import get_messages

class ProductModelTestCase(TestCase):
    def setUp(self):
        """Set up test data for Product model"""
        category = Category.objects.create(name='Electronics', friendly_name='Electronics')
        self.product = Product.objects.create(
            category=category,
            sku='12345',
            name='Test Product',
            description='A test product description.',
            price=50.00
        )
        # Create a user for review
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_average_review_rating_no_reviews(self):
        """Test the average rating with no reviews"""
        self.assertEqual(self.product.average_review_rating(), 0)

    def test_average_review_rating_with_reviews(self):
        """Test the average rating with reviews"""
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=5,
            comment='Great product!'
        )
        Review.objects.create(
            user=self.user,
            product=self.product,
            rating=4,
            comment='Good product.'
        )
        self.assertEqual(self.product.average_review_rating(), 4.5)


class AllProductsViewTestCase(TestCase):
    def setUp(self):
        """Set up test data for the all_products view"""
        category = Category.objects.create(name='Electronics', friendly_name='Electronics')
        self.product1 = Product.objects.create(
            category=category,
            sku='12345',
            name='Test Product 1',
            description='A test product.',
            price=50.00
        )
        self.product2 = Product.objects.create(
            category=category,
            sku='12346',
            name='Test Product 2',
            description='Another test product.',
            price=100.00
        )

    def test_all_products_view(self):
        """Test that all products are shown"""
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test Product 2')

    def test_product_sort_by_name(self):
        """Test that products are sorted by name"""
        response = self.client.get(reverse('products') + '?sort=name&direction=asc')
        self.assertContains(response, 'Test Product 1')
        self.assertContains(response, 'Test Product 2')

    def test_product_search(self):
        """Test the search functionality"""
        response = self.client.get(reverse('products') + '?q=Test Product 1')
        self.assertContains(response, 'Test Product 1')
        self.assertNotContains(response, 'Test Product 2')


class ProductDetailViewTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='password123'
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            category=self.category,
            name='Test Product',
            price=10.00,
            description='Test product description'
        )
        self.url = reverse('product_detail', args=[self.product.id])

    def test_submit_review(self):
        self.client.login(username='testuser', password='password123')

        # Prepare data for the review form
        data = {
            'rating': 5,
            'comment': 'Great product!'
        }

        # Submit the review
        response = self.client.post(self.url, data)

        # Check that the user is redirected
        self.assertEqual(response.status_code, 302)

        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.reviews.count(), 1)


        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Your review has been submitted!')

class ProductCRUDTestCase(TestCase):
    def setUp(self):
        # Set up a superuser for testing
        self.superuser = User.objects.create_superuser(
            username='admin', password='adminpassword')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            category=self.category,
            sku='12345',
            name='Test Product',
            description='Test description',
            price=9
        )

    def test_add_product(self):
        """Test adding a product"""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('add_product'), {
            'category': self.category.id,
            'sku': '12346',
            'name': 'New Product',
            'description': 'A new product description.',
            'price': 75.00,
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        new_product = Product.objects.get(name='New Product')
        self.assertEqual(new_product.price, 75.00)


    def test_edit_product(self):
        """Test editing a product"""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('edit_product', args=[self.product.id]), {
            'category': self.category.id,
            'sku': '12345',
            'name': 'Updated Product',
            'description': 'Updated description',
            'price': 7,
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')
        self.assertEqual(self.product.price, 7)

    def test_delete_product(self):
        """Test deleting a product"""
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('delete_product', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to products list
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=self.product.id)