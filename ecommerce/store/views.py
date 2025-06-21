from http.client import responses

import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from unicodedata import category

from .models import Order
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, OrderItem, Category
from django.conf import settings
from django.http import JsonResponse


# Register views.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now login.")
        return redirect('login.')
    else:
        form = RegisterForm()
        return render(request, 'store/register.html', {'form': form})


# Login views.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') # You can redirect to homepage
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'store/login.html')


# Logout View.
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def checkout_view(request):
    # logic here
    return render(request, 'store/checkout.html')


# Utility to get current order
def get_user_order(user):
    order, created = Order.objects.get_or_create(user=user, complete=False)
    return order


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order = get_user_order(request.user)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if not created:
        order_item.quantity += 1
    order_item.save()

    return redirect('view_cart')


@login_required
def view_cart(request):
    order = get_user_order(request.user)
    items = OrderItem.objects.filter(order=order)
    total = sum([item.product.price * item.quantity for item in items])

    context = {
        'items': items,
        'total': total
    }
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request):
    order = get_user_order(request.user)
    order.complete = True
    order.save()
    return render(request, 'store/checkout_success.html')


# Initiate Payment View.
@login_required
def initiate_payment(request):
    order = get_user_order(request.user)
    amount = sum([item.product.price *
                  item.quantity for item in OrderItem.objects.filter(order=order)])*100
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": request.user.email,
        "amount": int(amount),
        "callback_url": request.build_absolute_url('/payment/callback/'),
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", json=data,
                            headers=headers)
    res_data = response.json()

    if res_data.get('status'):
        auth_url = res_data['data']['authorization_url']
        return redirect(auth_url)
    else:
        return render(request, 'store/payment_failed.html',
                      {"error": "Could not initiate payment."})


@login_required
def payment_callback(request):
    reference = request.GET.get('reference')
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }
    response = requests.get(f"https://api.paystack.co/transaction/verify/{reference}", headers=headers)
    res_data = response.json()

    if requests.get('status') and res_data['data']['status'] == 'success':
        order = get_user_order(request.user)
        items = OrderItem.objects.filter(order=order)
        for item in items:
            item.product.stock -= item.quantity
            item.product.save()
        order.paid = True
        order.complete = True
        order.save()
        return render(request, 'store/payment_success.html')
    else:
        return render(request, 'store/payment_failed.html')


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, complete=True)
    return render(request, 'store/order_history.html', {'orders': orders})


def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('catrgory')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    return render(request, 'store/product_list.html',
                  {
                      'products': products,
                      'categories': categories,
                      'selected_category': category_id,
                      'query': query
                  })