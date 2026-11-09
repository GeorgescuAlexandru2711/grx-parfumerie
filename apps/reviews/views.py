from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.catalog.models import Product
from apps.orders.models import OrderItem
from .models import Review

@login_required
@require_POST
def add_review_view(request, product_id):
    """
    Enforces that only verified buyers who have paid for this perfume can leave a review (B3).
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if user purchased and paid for this perfume
    has_purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__payment_status='paid',
        variant__product=product
    ).exists()

    if not has_purchased and not request.user.is_staff:
        messages.error(request, "Only verified buyers who have purchased and paid for this fragrance can submit a review.")
        return redirect('catalog:product_detail', slug=product.slug)

    try:
        rating = int(request.POST.get('rating', 5))
    except (ValueError, TypeError):
        rating = 5

    rating = max(1, min(5, rating))
    title = request.POST.get('title', '').strip()
    comment = request.POST.get('comment', '').strip()

    if not comment:
        messages.error(request, "Please share a few words about your fragrance experience.")
        return redirect('catalog:product_detail', slug=product.slug)

    review, created = Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            'rating': rating,
            'title': title or f"{rating} Star Review",
            'comment': comment,
            'is_verified_purchase': True,
            'is_approved': True,
        }
    )

    if created:
        messages.success(request, "Thank you! Your verified review has been published.")
    else:
        messages.success(request, "Your fragrance review has been updated.")

    return redirect('catalog:product_detail', slug=product.slug)
