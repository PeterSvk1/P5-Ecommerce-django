from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm, NewsletterPostForm
from django.core.mail import send_mail
from django.conf import settings
from .models import NewsletterPost, NewsletterSubscription
from django.contrib.auth.decorators import login_required


def subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if NewsletterSubscription.objects.filter(email=email).exists():
                messages.error(request, 'Error: You are already subscribed!')
                return render(request, 'home.html', {'form': form})

            form.save()

            subject = 'Subscription Confirmation'
            message = 'Thank you for subscribing to our newsletter!'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.success(
                request,
                'Thank you for subscribing! An email has been sent to '
                'confirm your subscription.'
                )
            return redirect('home')
        else:
            messages.error(request, 'Already subscribed!')

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
