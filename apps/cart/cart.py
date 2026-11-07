from decimal import Decimal
from django.conf import settings
from apps.catalog.models import ProductVariant, Product

FREE_SHIPPING_THRESHOLD = Decimal('300.00')
STANDARD_SHIPPING_FEE = Decimal('20.00')

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                'items': {},
                'samples': [],
                'coupon': None,
            }
        self.cart = cart

    def add(self, variant, quantity=1, override_quantity=False):
        variant_id = str(variant.id)
        items = self.cart['items']

        if variant_id not in items:
            items[variant_id] = {
                'quantity': 0,
                'price': str(variant.price),
            }

        if override_quantity:
            items[variant_id]['quantity'] = max(1, min(quantity, variant.stock_quantity))
        else:
            new_qty = items[variant_id]['quantity'] + quantity
            items[variant_id]['quantity'] = min(new_qty, variant.stock_quantity)

        self.save()

    def remove(self, variant):
        variant_id = str(variant.id)
        if variant_id in self.cart['items']:
            del self.cart['items'][variant_id]
            self.save()

    def set_samples(self, sample_ids):
        """Allow customer to choose up to 2 free discovery vials (Douglas feature)."""
        valid_samples = list(sample_ids[:2])
        self.cart['samples'] = valid_samples
        self.save()

    def set_coupon(self, coupon_code, discount_percent):
        self.cart['coupon'] = {
            'code': coupon_code,
            'percent': discount_percent,
        }
        self.save()

    def remove_coupon(self):
        self.cart['coupon'] = None
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {
            'items': {},
            'samples': [],
            'coupon': None,
        }
        self.save()

    def __iter__(self):
        variant_ids = self.cart['items'].keys()
        variants = ProductVariant.objects.filter(id__in=variant_ids).select_related('product', 'product__brand')

        cart_items = self.cart['items'].copy()
        for variant in variants:
            cart_items[str(variant.id)]['variant'] = variant

        for item in cart_items.values():
            if 'variant' in item:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart['items'].values())

    def get_subtotal(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart['items'].values()
        )

    def get_discount_amount(self):
        coupon = self.cart.get('coupon')
        if not coupon:
            return Decimal('0.00')
        percent = Decimal(str(coupon.get('percent', 0)))
        subtotal = self.get_subtotal()
        return round((subtotal * percent) / Decimal('100.00'), 2)

    def get_shipping_fee(self):
        subtotal = self.get_subtotal()
        if subtotal == 0 or subtotal >= FREE_SHIPPING_THRESHOLD:
            return Decimal('0.00')
        return STANDARD_SHIPPING_FEE

    def get_total(self):
        subtotal = self.get_subtotal()
        if subtotal == 0:
            return Decimal('0.00')
        discount = self.get_discount_amount()
        shipping = self.get_shipping_fee()
        return max(Decimal('0.00'), (subtotal - discount) + shipping)

    def get_sample_products(self):
        sample_ids = self.cart.get('samples', [])
        if not sample_ids:
            return []
        return Product.objects.filter(id__in=sample_ids)[:2]
