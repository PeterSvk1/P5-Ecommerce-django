
from django.contrib import admin
from .models import NewsletterSubscription, NewsletterPost


@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    ordering = ('-subscribed_at',)


@admin.register(NewsletterPost)
class NewsletterPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    ordering = ('-published_date',)
