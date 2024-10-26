from django import forms
from .models import Review, ContactMessage  

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','rating']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write your review here...',
                'class': 'form-control',
            }),
            'rating': forms.Select(
                choices=[(i/10, str(i/10)) for i in range(10, 51, 10)])
        }

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'id': 'name' 
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
            'id': 'email'
        })
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message here',
            'rows': 5,
            'id': 'message'
        })
    )