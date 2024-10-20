from django import forms
from .models import Review

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