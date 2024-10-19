
from django.urls import path
from .views import submit_review

urlpatterns = [
    path('submit-review/<int:product_id>/', submit_review, name='submit_review'),
]