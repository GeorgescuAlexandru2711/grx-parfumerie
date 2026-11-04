from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Product, ProductVariant, Category, Brand, FragranceFamily

def home_view(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True).prefetch_related('variants', 'brand', 'category')[:8]
    categories = Category.objects.all()
    fragrance_families = FragranceFamily.objects.all()[:6]
    latest_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]

    return render(request, 'catalog/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'fragrance_families': fragrance_families,
        'latest_arrivals': latest_arrivals,
    })


def catalog_view(request):
    """
    Comprehensive catalog view with multi-faceted filtering (A1).
    """
    products = Product.objects.filter(is_active=True).prefetch_related('variants', 'brand', 'category', 'fragrance_family')

    # Filters
    category_slug = request.GET.get('category')
    family_slug = request.GET.get('family')
    brand_slug = request.GET.get('brand')
    sort_by = request.GET.get('sort', 'featured')
    in_stock_only = request.GET.get('in_stock') == '1'

    selected_category = None
    selected_family = None
    selected_brand = None

    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)

    if family_slug:
        selected_family = get_object_or_404(FragranceFamily, slug=family_slug)
        products = products.filter(fragrance_family=selected_family)

    if brand_slug:
        selected_brand = get_object_or_404(Brand, slug=brand_slug)
        products = products.filter(brand=selected_brand)

    if in_stock_only:
        products = products.filter(variants__stock_quantity__gt=0).distinct()

    # Sorting
    if sort_by == 'price_asc':
        products = products.order_by('variants__price').distinct()
    elif sort_by == 'price_desc':
        products = products.order_by('-variants__price').distinct()
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-is_featured', 'title')

    all_categories = Category.objects.all()
    all_families = FragranceFamily.objects.all()
    all_brands = Brand.objects.all()

    return render(request, 'catalog/catalog.html', {
        'products': products,
        'categories': all_categories,
        'families': all_families,
        'brands': all_brands,
        'selected_category': selected_category,
        'selected_family': selected_family,
        'selected_brand': selected_brand,
        'sort_by': sort_by,
        'in_stock_only': in_stock_only,
    })


def search_view(request):
    """
    Search by perfume title, brand, notes, or olfactory family (A2).
    """
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(top_notes__icontains=query) |
            Q(heart_notes__icontains=query) |
            Q(base_notes__icontains=query) |
            Q(short_description__icontains=query) |
            Q(fragrance_family__name__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).distinct()

    return render(request, 'catalog/search.html', {
        'query': query,
        'products': products,
        'result_count': products.count(),
    })


def category_detail_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'selected_category': category,
        'categories': Category.objects.all(),
        'families': FragranceFamily.objects.all(),
        'brands': Brand.objects.all(),
    })


def fragrance_family_detail_view(request, family_slug):
    family = get_object_or_404(FragranceFamily, slug=family_slug)
    products = Product.objects.filter(fragrance_family=family, is_active=True)
    return render(request, 'catalog/catalog.html', {
        'products': products,
        'selected_family': family,
        'categories': Category.objects.all(),
        'families': FragranceFamily.objects.all(),
        'brands': Brand.objects.all(),
    })


def product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category', 'fragrance_family').prefetch_related('variants', 'reviews__user'),
        slug=slug,
        is_active=True
    )
    variants = product.variants.all().order_by('price')
    default_variant = product.default_variant

    # Check if logged-in user is a verified buyer (B3)
    user_is_verified_buyer = False
    user_has_reviewed = False
    if request.user.is_authenticated:
        from apps.orders.models import OrderItem
        user_is_verified_buyer = OrderItem.objects.filter(
            order__user=request.user,
            order__payment_status='paid',
            variant__product=product
        ).exists()
        user_has_reviewed = product.reviews.filter(user=request.user).exists()

    approved_reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')

    # Related recommendations in same fragrance family or category
    related_products = Product.objects.filter(
        Q(fragrance_family=product.fragrance_family) | Q(category=product.category),
        is_active=True
    ).exclude(pk=product.pk)[:4]

    return render(request, 'catalog/detail.html', {
        'product': product,
        'variants': variants,
        'default_variant': default_variant,
        'user_is_verified_buyer': user_is_verified_buyer,
        'user_has_reviewed': user_has_reviewed,
        'reviews': approved_reviews,
        'related_products': related_products,
    })
