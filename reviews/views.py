from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ContactForm
from .models import ContactMessage
import os

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(request, 'There was a problem with your submission.')
    else:
        form = ReviewForm()

    return render(request, 'reviews/review_form.html', {'form': form, 'product': product})

def reviews_list_view(request):
    reviews = Review.objects.all().select_related('product', 'user')
    return render(request, 'reviews/reviews_list.html', {'reviews': reviews})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract the cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Create and save a ContactMessage instance
            contact_message = ContactMessage(name=name, email=email, message=message)
            contact_message.save()
            
            # Send the email to the designated recipient
            send_mail(
                f'Message from {name}',
                message,
                email,  # From email
                [os.environ.get('EMAIL_HOST_USER')],  # To email
            )
            
            # Send a confirmation email to the sender
            confirmation_subject = 'We have received your message!'
            confirmation_message = f'Hello {name},\n\nThank you for reaching out to us! We have received your message:\n\n"{message}"\n\nWe will get back to you shortly.\n\nBest regards,\nYour Team'
            send_mail(
                confirmation_subject,
                confirmation_message,
                os.environ.get('EMAIL_HOST_USER'),  # From your email
                [email],  # To sender's email
            )

            messages.success(request, 'Your message has been sent!')
            return redirect('contact')  # Redirect to the same page or another page
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})