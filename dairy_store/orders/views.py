from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Import messages for flash messages
from django.conf import settings  # Added import for settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

from .models import Order, OrderItem, Payment
from cart.models import Cart, CartItem  # Assuming Cart model exists in cart app

import razorpay

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# def send_order_confirmation_email(order):
    # subject = f'Order Confirmation - #{order.id}'
    # html_message = render_to_string('order_confirmation_email.html', {'order': order, 'user': order.user})
    # plain_message = strip_tags(html_message)
    # from_email = settings.DEFAULT_FROM_EMAIL
    # to = order.user.email

    # send_mail(subject, plain_message, from_email, [to], html_message=html_message)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    # Get the user's cart and items
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('home')

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Validate form fields here if you want

        # Create the order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            payment_method=payment_method,
            total_price=total_amount,
            status='Pending',
            created_at=timezone.now(),
        )

        # Create order items from cart items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,  # Capture the price at order time
            )

        # Clear cart items
        cart_items.delete()
        # Optionally delete cart as well: cart.delete()

        messages.success(request, "Order placed successfully!")

        # Redirect to order confirmation page
        return redirect('order_confirmation_view', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'orders/checkout.html', context)




@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save()
        messages.success(request, "Order cancelled successfully.")
    else:
        messages.error(request, "Order cannot be cancelled.")
    return redirect('orders/order_detail', order_id=order.id)

from django.shortcuts import render, get_object_or_404
from .models import Order

def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_confirmation_view.html', {'order': order})
# Payment verification view
@csrf_exempt  # Usually payment gateways send POST without CSRF token
def payment_verify(request):
    if request.method == "POST":
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        order_id = request.POST.get('order_id')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('orders/order_detail', order_id=order_id)

        try:
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        except Payment.DoesNotExist:
            messages.error(request, "Payment record not found.")
            return redirect('orders/order_detail', order_id=order_id)

        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'Paid'
        payment.save()

        order = payment.order
        order.status = 'Processing'
        order.save()

        messages.success(request, "Payment successful! Your order is now processing.")
        return redirect('orders/order_detail', order_id=order.id)

    return HttpResponseBadRequest()
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import CancelOrderForm, ReturnOrderForm

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Pending', is_cancelled=False)
    if request.method == 'POST':
        form = CancelOrderForm(request.POST)
        if form.is_valid():
            order.is_cancelled = True
            order.cancelled_at = timezone.now()
            order.cancellation_reason = form.cleaned_data['reason']
            order.status = 'Cancelled'
            order.save()
            messages.success(request, "Order cancelled successfully.")
            return redirect('order_history')
    else:
        form = CancelOrderForm()
    return render(request, 'orders/cancel_order.html', {'form': form, 'order': order})

@login_required
def return_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user, status='Delivered', is_returned=False)
    if request.method == 'POST':
        form = ReturnOrderForm(request.POST)
        if form.is_valid():
            order.is_returned = True
            order.returned_at = timezone.now()
            order.return_reason = form.cleaned_data['reason']
            order.save()
            messages.success(request, "Return request submitted successfully.")
            return redirect('order_history')
    else:
        form = ReturnOrderForm()
    return render(request, 'orders/return_order.html', {'form': form, 'order': order})
