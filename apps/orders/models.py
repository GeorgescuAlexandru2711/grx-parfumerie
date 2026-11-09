import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from apps.catalog.models import ProductVariant, Product

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Payment'
        PAID = 'paid', 'Paid'
        PROCESSING = 'processing', 'Processing & Packaging'
        SHIPPED = 'shipped', 'Shipped'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentStatus(models.TextChoices):
        UNPAID = 'unpaid', 'Unpaid'
        PAID = 'paid', 'Paid'
        FAILED = 'failed', 'Payment Failed'
        REFUNDED = 'refunded', 'Refunded'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_number = models.CharField(max_length=40, unique=True, editable=False)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)

    # Customer & Shipping details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=25)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100, verbose_name="County / Sector")
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=60, default='Romania')
    order_notes = models.TextField(blank=True)

    # Free discovery samples (Douglas feature)
    sample_1 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')
    sample_2 = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='+')

    # Financial breakdown (in RON)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    coupon_code = models.CharField(max_length=50, blank=True)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Stripe tracking (A6)
    stripe_session_id = models.CharField(max_length=255, blank=True)
    stripe_payment_intent = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} ({self.total_amount} RON)"

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"GRX-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_paid(self):
        return self.payment_status == self.PaymentStatus.PAID


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, related_name='order_items')

    # Historical snapshot to preserve record even if catalog changes
    product_title = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=120)
    size_label = models.CharField(max_length=50)
    sku = models.CharField(max_length=60)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_title} ({self.size_label})"

    def save(self, *args, **kwargs):
        if not self.line_total:
            self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)
