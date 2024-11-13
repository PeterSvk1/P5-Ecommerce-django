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
            form.save()

            email = form.cleaned_data['email']
            subject = 'Subscription Confirmation'
            message = 'Thank you for subscribing to our newsletter!'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(request, 'Thank you for subscribing! An email has been sent to confirm your subscription.')
            return redirect('home')
        else:
            messages.error(request, 'Error: Already subscribed!.')

    return redirect('home')

def newsletter_list(request):
    newsletters = NewsletterPost.objects.all().order_by('-published_date')
    return render(request, 'newsletter.html', {'newsletters': newsletters})

@login_required
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterPostForm(request.POST)
        if form.is_valid():
            newsletter = form.save(commit=False)
            newsletter.author = request.user
            newsletter.save()
            messages.success(request, 'Newsletter created successfully!')
            return redirect('newsletter_list')
    else:
        form = NewsletterPostForm()

    return render(request, 'create_newsletter.html', {'form': form})
