from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product  # Make sure this imports your Product model

# ----------------- DASHBOARD -----------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from orders.models import Order  # Adjust according to your app names

@login_required
def dashboard(request):
    user = request.user
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]

    context = {
        'user': user,
        'recent_orders': recent_orders,
    }
    return render(request, 'core/dashboard.html', context)
# ----------------- HOME VIEW -----------------
def home(request):
    if not request.user.is_authenticated:
        return redirect('signup')
        return redirect('dashboard')
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name_icontains=query) | Q(description_icontains=query)
        )

    return render(request, 'core/home.html', {
        'products': products,
        'query': query
    })

# ----------------- PRODUCT DETAIL -----------------
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    similar_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return render(request, 'core/product_detail.html', {
        'product': product,
        'similar_products': similar_products
    })

# ----------------- SIGNUP -----------------
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
# ----------------- PROFILE EDIT -----------------
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms

# Create a simple form for editing username and email
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'core/profile_edit.html', {'form': form})
