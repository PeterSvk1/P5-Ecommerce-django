
from django.urls import path
from .views import submit_review, reviews_list_view

urlpatterns = [
    path('submit-review/<int:product_id>/', submit_review, name='submit_review'),
    path('reviews/', reviews_list_view, name='reviews_list'),
]