from django import forms
from .models import NewsletterSubscription, NewsletterPost

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']


class NewsletterPostForm(forms.ModelForm):
    class Meta:
        model = NewsletterPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the title of the newsletter',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your content here...',
                'rows': 8,
            }),
        }
        labels = {
            'title': 'Newsletter Title',
            'content': 'Content',
        }