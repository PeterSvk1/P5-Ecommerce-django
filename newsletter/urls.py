from django.urls import path
from .views import subscribe, newsletter_list, create_newsletter

urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('newsletters/', newsletter_list, name='newsletter_list'),
    path('newsletters/create/', create_newsletter, name='create_newsletter'),
]
