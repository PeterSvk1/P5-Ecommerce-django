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

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        bag[item_id] = quantity
        messages.success(request, f'Added {product.name} x {bag[item_id]} to your bag ')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)

def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""
    
    product = get_object_or_404(Product, pk=item_id)
    bag = request.session.get('bag', {})
    quantity = int(request.POST.get('quantity', 0))

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
    else:
        if item_id in bag:
            bag.pop(item_id, None)
            messages.success(request, f'Removed {product.name} from your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))
