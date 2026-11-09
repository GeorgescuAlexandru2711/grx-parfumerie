from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, blank=True, help_text="Lucide or Heroicon name")

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:category_detail', kwargs={'category_slug': self.slug})


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    origin_country = models.CharField(max_length=60, default='France')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class FragranceFamily(models.Model):
    name = models.CharField(max_length=80, unique=True)  # Woody, Oriental, Floral, Fresh, Gourmand
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Fragrance Families'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    class Concentration(models.TextChoices):
        EDT = 'EDT', 'Eau de Toilette'
        EDP = 'EDP', 'Eau de Parfum'
        EXTRAIT = 'EXTRAIT', 'Extrait de Parfum'
        COLOGNE = 'COLOGNE', 'Eau de Cologne'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    fragrance_family = models.ForeignKey(FragranceFamily, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    concentration = models.CharField(max_length=20, choices=Concentration.choices, default=Concentration.EDP)

    short_description = models.CharField(max_length=280, help_text="Quick olfactory summary for cards")
    description = models.TextField()

    # Olfactory Pyramid (A1 Guided Discovery)
    top_notes = models.CharField(max_length=255, help_text="Opening notes, e.g. Bergamot, Saffron, Mandarin")
    heart_notes = models.CharField(max_length=255, help_text="Heart/Middle notes, e.g. Jasmine, Turkish Rose, Cardamom")
    base_notes = models.CharField(max_length=255, help_text="Base/Drydown notes, e.g. Ambergris, Cedarwood, Vanilla")

    image = models.ImageField(upload_to='products/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text="Fallback external image URL")

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', 'title']

    def __str__(self):
        return f"{self.brand.name} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.brand.name}-{self.title}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return 'https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?auto=format&fit=crop&w=800&q=80'

    @property
    def default_variant(self):
        variant = self.variants.filter(is_default=True).first()
        if not variant:
            variant = self.variants.order_by('price').first()
        return variant

    @property
    def min_price(self):
        variant = self.variants.order_by('price').first()
        return variant.price if variant else 0

    @property
    def total_stock(self):
        return sum(v.stock_quantity for v in self.variants.all())

    @property
    def in_stock(self):
        return self.total_stock > 0

    @property
    def average_rating(self):
        avg = self.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 5.0

    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()


class ProductVariant(models.Model):
    """
    Different bottle sizes:
    e.g. 10ml Travel Size, 50ml, 100ml.
    Critical for A7 (Stock Management with row-level locks).
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size_label = models.CharField(max_length=50, help_text="e.g. 10ml Travel Size, 50ml, 100ml, Gift Set")
    size_ml = models.PositiveIntegerField(help_text="Volume in ml (0 for sets)")
    sku = models.CharField(max_length=60, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in RON")
    stock_quantity = models.PositiveIntegerField(default=0, help_text="Available inventory units")
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['price']

    def __str__(self):
        return f"{self.product.title} - {self.size_label} ({self.price} RON)"

    @property
    def in_stock(self):
        return self.stock_quantity > 0
