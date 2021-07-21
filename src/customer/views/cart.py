# -*- coding: utf-8 -*-

from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from src.product.models import Product
from src.customer.cart import Cart
from src.customer.forms import CartQuantityForm


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartQuantityForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'], update_quantity=True)
    return redirect('customer-order')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('customer-order')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('customer-order')


def cart_add_ajax(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1, update_quantity=False)
    return JsonResponse({'status': 'success'})


def cart_update_ajax(request, product_id):
    print(request.GET.get('quantity').isdigit())
    if request.GET.get('quantity').isdigit():
        quantity = int(request.GET.get('quantity'))
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        stock = product.stocks.filter(
            warehouse_id=request.session[settings.WAREHOUSE_SESSION_ID]).first()
        if stock.in_stock < quantity:
            quantity = stock.in_stock
            messages.error(request, "%s бүтээгдэхүүний нөөц %s байна." %
                           (product.name, quantity))
        cart.add(product=product, quantity=quantity, update_quantity=True)
    return JsonResponse({'status': 'success'})


def cart_remove_ajax(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'cart_length': len(cart), 'cart_total': cart.get_total_price()})


def cart_header_ajax(request):
    return render(request, 'customer/include/cart.html')
