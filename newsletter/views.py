from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm, NewsletterPostForm
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterPost
from django.contrib.auth.decorators import login_required

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

def newsletter_list(request):
    newsletters = NewsletterPost.objects.all().order_by('-published_date')
    return render(request, 'newsletter.html', {'newsletters': newsletters})

@login_required
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterPostForm(request.POST)
        if form.is_valid():
            # Save the form but do not commit yet to add the author
            newsletter = form.save(commit=False)
            newsletter.author = request.user  # Set the author to the current logged-in user
            newsletter.save()
            messages.success(request, 'Newsletter created successfully!')
            return redirect('newsletter_list')  # Redirect to the list of newsletters
    else:
        form = NewsletterPostForm()

    return render(request, 'create_newsletter.html', {'form': form})
