from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.cart.cart import Cart
from .models import Order
from .forms import CheckoutForm
from .services import create_order_from_cart, InsufficientStockError

def checkout_view(request):
    """
    Checkout page (A5) with atomic order reservation and address validation.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.info(request, "Your bag is currently empty. Please add fragrances before checking out.")
        return redirect('catalog:list')

    # Initial values prefilled from user profile if logged in
    initial_data = {}
    if request.user.is_authenticated:
        u = request.user
        initial_data = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'phone_number': u.phone_number,
            'address_line1': u.address_line1,
            'address_line2': u.address_line2,
            'city': u.city,
            'county': u.county,
            'postal_code': u.postal_code,
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                # Create order with PostgreSQL row-level lock (select_for_update)
                order = create_order_from_cart(
                    cart=cart,
                    customer_data=form.cleaned_data,
                    user=request.user
                )

                # Store order ID in session for Stripe redirection
                request.session['checkout_order_id'] = order.id

                # Redirect to Stripe sandbox payment flow (A6)
                return redirect('payments:stripe_checkout', order_id=order.id)

            except InsufficientStockError as err:
                messages.error(request, str(err))
                return redirect('cart:detail')
            except Exception as e:
                messages.error(request, f"An unexpected error occurred during checkout: {e}")
    else:
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart,
        'samples': cart.get_sample_products(),
    })


def order_detail_view(request, order_number):
    """
    Display order receipt & status details.
    """
    order = get_object_or_404(Order.objects.prefetch_related('items'), order_number=order_number)

    # If order belongs to a user, restrict access to that user or staff
    if order.user and order.user != request.user and not request.user.is_staff:
        messages.error(request, "You are not authorized to view this order.")
        return redirect('catalog:home')

    return render(request, 'orders/order_detail.html', {
        'order': order,
    })


@login_required
def order_history_view(request):
    """
    Order history dashboard for logged-in customers (A8).
    """
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')

    return render(request, 'orders/order_history.html', {
        'orders': orders,
    })
