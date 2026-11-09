from .cart import Cart

def cart_context(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'cart_item_count': len(cart),
        'cart_subtotal': cart.get_subtotal(),
        'cart_total': cart.get_total(),
    }
