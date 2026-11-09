from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from apps.catalog.models import ProductVariant, Product
from .cart import Cart

# Valid server-side discount coupons (B5)
ACTIVE_COUPONS = {
    'WELCOME10': 10,     # 10% off for newcomers
    'AURELLE15': 15,     # 15% off launch special
    'LUXURY20': 20,      # 20% off for VIP customers
}

def cart_detail_view(request):
    cart = Cart(request)
    sample_candidates = Product.objects.filter(is_active=True).select_related('brand')[:12]
    selected_samples = cart.get_sample_products()

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'sample_candidates': sample_candidates,
        'selected_samples': selected_samples,
    })


@require_POST
def cart_add_view(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        quantity = 1

    if variant.stock_quantity <= 0:
        messages.error(request, f"Sorry, {variant.product.title} ({variant.size_label}) is currently out of stock.")
        return redirect('catalog:product_detail', slug=variant.product.slug)

    # Check cart existing quantity
    current_in_cart = cart.cart['items'].get(str(variant.id), {}).get('quantity', 0)
    if current_in_cart + quantity > variant.stock_quantity:
        allowed = max(0, variant.stock_quantity - current_in_cart)
        if allowed > 0:
            cart.add(variant, quantity=allowed)
            messages.warning(request, f"Added {allowed} units of {variant.product.title} ({variant.size_label}). Maximum available stock reached.")
        else:
            messages.warning(request, f"You already have all available units of {variant.product.title} in your cart.")
    else:
        cart.add(variant, quantity=quantity)
        messages.success(request, f"Added {variant.product.title} ({variant.size_label}) to your bag.")

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': float(cart.get_total()),
        })

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart:detail'
    return redirect(next_url)


@require_POST
def cart_update_view(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        cart.remove(variant)
        messages.info(request, f"Removed {variant.product.title} from your bag.")
    else:
        if quantity > variant.stock_quantity:
            cart.add(variant, quantity=variant.stock_quantity, override_quantity=True)
            messages.warning(request, f"Only {variant.stock_quantity} units available for {variant.product.title}.")
        else:
            cart.add(variant, quantity=quantity, override_quantity=True)
            messages.success(request, f"Updated quantity for {variant.product.title}.")

    return redirect('cart:detail')


@require_POST
def cart_remove_view(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart.remove(variant)
    messages.info(request, f"Removed {variant.product.title} ({variant.size_label}) from your bag.")
    return redirect('cart:detail')


@require_POST
def cart_samples_view(request):
    """
    Save chosen free fragrance samples (up to 2).
    """
    cart = Cart(request)
    sample_ids = request.POST.getlist('sample_ids')
    cart.set_samples(sample_ids)
    messages.success(request, "Your complimentary fragrance discovery samples have been selected.")
    return redirect('cart:detail')


@require_POST
def apply_coupon_view(request):
    """
    Server-side discount coupon validation (B5).
    """
    cart = Cart(request)
    code = request.POST.get('coupon_code', '').strip().upper()

    if not code:
        messages.error(request, "Please enter a coupon code.")
        return redirect('cart:detail')

    if code in ACTIVE_COUPONS:
        discount = ACTIVE_COUPONS[code]
        cart.set_coupon(code, discount)
        messages.success(request, f"Coupon '{code}' applied successfully! {discount}% off your order.")
    else:
        messages.error(request, f"Invalid or expired coupon code: '{code}'.")

    return redirect('cart:detail')


@require_POST
def remove_coupon_view(request):
    cart = Cart(request)
    cart.remove_coupon()
    messages.info(request, "Coupon removed.")
    return redirect('cart:detail')
