
from django.urls import path
from .views import submit_review, reviews_list_view, contact_view
from .views import delete_review
urlpatterns = [
    path(
        'submit-review/<int:product_id>/',
        submit_review, name='submit_review'),
    path('reviews/', reviews_list_view, name='reviews_list'),
    path('contact/', contact_view, name='contact'),
    path('delete-review/<int:review_id>/', delete_review, name='delete_review'),
]
