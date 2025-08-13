from .models import CartItem

def cart_totals(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        total_quantity = sum(item.quantity for item in cart_items)
        return {'cart_total_amount': total_amount, 'cart_total_quantity': total_quantity}
    return {}