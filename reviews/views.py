from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from products.models import Product
from django.contrib.auth.decorators import login_required

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