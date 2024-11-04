from django.urls import path
from .views import subscribe, newsletter_list
urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('newsletters/', newsletter_list, name='newsletter_list'),
]