from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.db import transaction

from apps.catalog.models import Product, ProductVariant, Brand, Category, FragranceFamily
from apps.orders.models import Order, OrderItem
from apps.accounts.models import User
from .forms import ProductForm, VariantForm, QuickRestockForm

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.role == User.Role.ADMIN or user.is_superuser)

admin_required = user_passes_test(is_admin, login_url='/accounts/login/')


@admin_required
def dashboard_overview(request):
    """
    Command Center Overview (A9)
    Displays revenue, order counts, stock status, and recent orders.
    """
    total_revenue = Order.objects.filter(payment_status=Order.PaymentStatus.PAID).aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')
    total_orders = Order.objects.count()
    paid_orders = Order.objects.filter(payment_status=Order.PaymentStatus.PAID).count()
    pending_orders = Order.objects.filter(status=Order.Status.PENDING).count()
    total_customers = User.objects.filter(role=User.Role.CUSTOMER).count()

    # Low stock alert: variants with 5 or fewer items remaining (A7)
    low_stock_variants = ProductVariant.objects.filter(stock_quantity__lte=5).select_related('product', 'product__brand').order_by('stock_quantity')[:10]
    low_stock_count = ProductVariant.objects.filter(stock_quantity__lte=5).count()

    # Recent orders
    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:8]

    # Category product distribution
    category_stats = Category.objects.annotate(product_count=Count('products')).order_by('-product_count')

    return render(request, 'dashboard/overview.html', {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'pending_orders': pending_orders,
        'total_customers': total_customers,
        'low_stock_count': low_stock_count,
        'low_stock_variants': low_stock_variants,
        'recent_orders': recent_orders,
        'category_stats': category_stats,
    })


@admin_required
def dashboard_products(request):
    """
    Product inventory and catalogue management table (A9).
    """
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    brand_id = request.GET.get('brand')

    products = Product.objects.select_related('brand', 'category', 'fragrance_family').prefetch_related('variants').order_by('-created_at')

    if query:
        products = products.filter(
            Q(title__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(variants__sku__icontains=query)
        ).distinct()

    if category_id:
        products = products.filter(category_id=category_id)
    if brand_id:
        products = products.filter(brand_id=brand_id)

    return render(request, 'dashboard/products.html', {
        'products': products,
        'categories': Category.objects.all(),
        'brands': Brand.objects.all(),
        'query': query,
    })


@admin_required
def dashboard_product_create(request):
    """
    Add a new curated fragrance to the catalog.
    """
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Fragrance '{product.title}' created successfully! Now add sizes/pricing variants.")
            return redirect('dashboard:product_edit', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'title': 'Add New Curated Fragrance',
    })


@admin_required
def dashboard_product_edit(request, pk):
    """
    Edit existing fragrance and manage its volume variants (10ml, 50ml, 100ml).
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST' and 'update_product' in request.POST:
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated '{product.title}'.")
            return redirect('dashboard:product_edit', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    variant_form = VariantForm()
    variants = product.variants.all().order_by('price')

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'product': product,
        'variant_form': variant_form,
        'variants': variants,
        'title': f"Edit {product.brand.name} - {product.title}",
    })


@admin_required
@require_POST
def dashboard_variant_add(request, product_id):
    """
    Add a new size variant (e.g. 10ml travel size) to a product.
    """
    product = get_object_or_404(Product, id=product_id)
    form = VariantForm(request.POST)
    if form.is_valid():
        variant = form.save(commit=False)
        variant.product = product
        if variant.is_default:
            product.variants.update(is_default=False)
        variant.save()
        messages.success(request, f"Added size variant '{variant.size_label}' ({variant.price} RON, {variant.stock_quantity} units).")
    else:
        messages.error(request, f"Failed to add variant: {form.errors}")

    return redirect('dashboard:product_edit', pk=product.id)


@admin_required
@require_POST
def dashboard_variant_delete(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    product_id = variant.product_id
    variant.delete()
    messages.info(request, f"Deleted variant '{variant.size_label}'.")
    return redirect('dashboard:product_edit', pk=product_id)


@admin_required
@require_POST
def dashboard_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    title = product.title
    product.delete()
    messages.success(request, f"Fragrance '{title}' has been removed from the catalogue.")
    return redirect('dashboard:products')


@admin_required
def dashboard_orders(request):
    """
    Order management dashboard (A9).
    """
    status_filter = request.GET.get('status')
    orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')

    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'dashboard/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order.Status.choices,
    })


@admin_required
def dashboard_order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('items', 'items__variant'), pk=pk)
    return render(request, 'dashboard/order_detail.html', {
        'order': order,
        'status_choices': Order.Status.choices,
        'payment_status_choices': Order.PaymentStatus.choices,
    })


@admin_required
@require_POST
def dashboard_order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    new_payment_status = request.POST.get('payment_status')

    if new_status in dict(Order.Status.choices):
        order.status = new_status
    if new_payment_status in dict(Order.PaymentStatus.choices):
        order.payment_status = new_payment_status

    order.save()
    messages.success(request, f"Order #{order.order_number} status updated to {order.get_status_display()}.")
    return redirect('dashboard:order_detail', pk=order.pk)


@admin_required
def dashboard_inventory(request):
    """
    Stock management and instant replenishment interface (A7, A9).
    """
    variants = ProductVariant.objects.select_related('product', 'product__brand').order_by('stock_quantity')
    restock_form = QuickRestockForm()

    return render(request, 'dashboard/inventory.html', {
        'variants': variants,
        'restock_form': restock_form,
    })


@admin_required
@require_POST
def dashboard_inventory_restock(request):
    """
    Atomically add inventory units to a variant.
    """
    form = QuickRestockForm(request.POST)
    if form.is_valid():
        variant_id = form.cleaned_data['variant_id']
        add_units = form.cleaned_data['add_units']

        with transaction.atomic():
            variant = ProductVariant.objects.select_for_update().get(id=variant_id)
            variant.stock_quantity += add_units
            variant.save(update_fields=['stock_quantity'])

        messages.success(request, f"Added {add_units} units to '{variant.product.title} ({variant.size_label})'. New stock: {variant.stock_quantity}.")
    else:
        messages.error(request, "Invalid restock request.")

    return redirect('dashboard:inventory')


@admin_required
def dashboard_customers(request):
    """
    Customer overview and spending insights.
    """
    customers = User.objects.filter(role=User.Role.CUSTOMER).annotate(
        order_count=Count('orders'),
        total_spent=Sum('orders__total_amount', filter=Q(orders__payment_status=Order.PaymentStatus.PAID))
    ).order_by('-date_joined')

    return render(request, 'dashboard/customers.html', {
        'customers': customers,
    })
