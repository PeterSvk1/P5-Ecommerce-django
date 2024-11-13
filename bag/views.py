from django.shortcuts import render, redirect, reverse, get_object_or_404

from django.contrib import messages
from products.models import Product

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    current_quantity = bag.get(item_id, 0)
    new_quantity = current_quantity + quantity

    if new_quantity > 5:
        bag[item_id] = 5
        messages.error(
            request,
            f'Sorry, max of 5 items per user {product.name} in your bag.'
            )
    else:
        bag[item_id] = new_quantity
        messages.success(
            request,
            f'Added {quantity} more {product.name} to your bag.'
            f'Total: {bag[item_id]}'
            )

    request.session['bag'] = bag

    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.name} quantity to {bag[item_id]}'
            )
    else:
        if item_id in bag:
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
