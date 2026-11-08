from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from apps.catalog.models import ProductVariant, Product
from .models import Order, OrderItem

class InsufficientStockError(Exception):
    """Raised when an item does not have enough stock during atomic checkout."""
    pass


def create_order_from_cart(cart, customer_data, user=None):
    """
    Atomically creates an order from the cart, utilizing PostgreSQL row-level locks
    (select_for_update) to guarantee no two concurrent shoppers can purchase the last unit.
    (Mitigates Risk 2 / Requirement A7).
    """
    if len(cart) == 0:
        raise ValueError("Cannot checkout with an empty cart.")

    sample_products = cart.get_sample_products()
    sample_1 = sample_products[0] if len(sample_products) > 0 else None
    sample_2 = sample_products[1] if len(sample_products) > 1 else None

    coupon = cart.cart.get('coupon')
    coupon_code = coupon.get('code', '') if coupon else ''

    with transaction.atomic():
        # First pass: lock all required variants and inspect inventory
        items_to_process = []
        for item in cart:
            variant_obj = item['variant']
            qty = item['quantity']

            # Row-level lock to prevent concurrent race condition (A7)
            locked_variant = ProductVariant.objects.select_for_update().get(id=variant_obj.id)

            if locked_variant.stock_quantity < qty:
                raise InsufficientStockError(
                    f"Only {locked_variant.stock_quantity} unit(s) remaining for "
                    f"'{locked_variant.product.title} ({locked_variant.size_label})'. "
                    f"Another customer may have just ordered the last unit."
                )

            items_to_process.append((locked_variant, qty, item['price']))

        # Create Order record
        order = Order.objects.create(
            user=user if (user and user.is_authenticated) else None,
            first_name=customer_data.get('first_name', ''),
            last_name=customer_data.get('last_name', ''),
            email=customer_data.get('email', ''),
            phone_number=customer_data.get('phone_number', ''),
            address_line1=customer_data.get('address_line1', ''),
            address_line2=customer_data.get('address_line2', ''),
            city=customer_data.get('city', ''),
            county=customer_data.get('county', ''),
            postal_code=customer_data.get('postal_code', ''),
            country=customer_data.get('country', 'Romania'),
            order_notes=customer_data.get('order_notes', ''),
            sample_1=sample_1,
            sample_2=sample_2,
            subtotal=cart.get_subtotal(),
            discount_amount=cart.get_discount_amount(),
            coupon_code=coupon_code,
            shipping_fee=cart.get_shipping_fee(),
            total_amount=cart.get_total(),
            status=Order.Status.PENDING,
            payment_status=Order.PaymentStatus.UNPAID,
        )

        # Create order items and decrement stock atomically
        for locked_variant, qty, price in items_to_process:
            OrderItem.objects.create(
                order=order,
                variant=locked_variant,
                product_title=locked_variant.product.title,
                brand_name=locked_variant.product.brand.name,
                size_label=locked_variant.size_label,
                sku=locked_variant.sku,
                unit_price=price,
                quantity=qty,
                line_total=price * qty,
            )

            # Decrement stock under row lock
            locked_variant.stock_quantity -= qty
            locked_variant.save(update_fields=['stock_quantity'])

    return order


def mark_order_as_paid(order, stripe_session_id='', stripe_payment_intent=''):
    """
    Confirms payment from Stripe webhook and transitions status to PAID (A6).
    """
    with transaction.atomic():
        locked_order = Order.objects.select_for_update().get(id=order.id)
        if locked_order.payment_status != Order.PaymentStatus.PAID:
            locked_order.payment_status = Order.PaymentStatus.PAID
            locked_order.status = Order.Status.PAID
            locked_order.paid_at = timezone.now()
            if stripe_session_id:
                locked_order.stripe_session_id = stripe_session_id
            if stripe_payment_intent:
                locked_order.stripe_payment_intent = stripe_payment_intent
            locked_order.save()
    return locked_order


def restore_order_stock(order):
    """
    Restores stock if checkout is cancelled or payment fails.
    """
    with transaction.atomic():
        locked_order = Order.objects.select_for_update().get(id=order.id)
        if locked_order.payment_status != Order.PaymentStatus.PAID and locked_order.status != Order.Status.CANCELLED:
            for item in locked_order.items.select_related('variant'):
                if item.variant:
                    locked_variant = ProductVariant.objects.select_for_update().get(id=item.variant.id)
                    locked_variant.stock_quantity += item.quantity
                    locked_variant.save(update_fields=['stock_quantity'])
            locked_order.status = Order.Status.CANCELLED
            locked_order.save()
