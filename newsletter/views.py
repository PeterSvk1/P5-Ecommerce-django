from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm
from django.core.mail import send_mail
from django.conf import settings

def subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            # Save the subscription
            form.save()

            # Send confirmation email
            email = form.cleaned_data['email']
            subject = 'Subscription Confirmation'
            message = 'Thank you for subscribing to our newsletter!'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Use the email defined in settings
                [email],
                fail_silently=False,
            )

            # Use a success message for toast notification
            messages.success(request, 'Thank you for subscribing! An email has been sent to confirm your subscription.')
            return redirect('home')  # Redirect to the home page or another page
        else:
            # Use an error message for toast notification
            messages.error(request, 'Please enter a valid email address.')

    return redirect('home')