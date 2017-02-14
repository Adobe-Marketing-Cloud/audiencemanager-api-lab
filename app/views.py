from django.shortcuts import render
from django.shortcuts import redirect
from django.core import serializers
from .app import AppConfig
from .models import *
import json


CART = 'cart'
ADD = 'add'
REMOVE = 'remove'


def to_json(object):
    json_string = serializers.serialize("json", object)
    return json.loads(json_string)


def initialize_cart(request):
    if CART not in request.session:
        request.session[CART] = []
        request.session.save()
    return request.session[CART]


def organize_cart(request):
    cart_list_orig = initialize_cart(request)
    quantity_map = {}
    for product in cart_list_orig:
        qty = get_product_qty(product)
        if product in quantity_map:
            quantity_map[product] += qty
        else:
            quantity_map[product] = qty

    cart_list = []
    for product in quantity_map:
        product.quantity = quantity_map[product]
        print(product, product.quantity)
        cart_list.append(product)

    request.session[CART] = cart_list
    request.session.save()
    return cart_list


def get_product_qty(product):
    if hasattr(product, 'quantity'):
        return product.quantity
    else:
        return 1


def get_cart_count(request):
    cart_list = initialize_cart(request)
    cart_count = 0
    for product in cart_list:
        cart_count += get_product_qty(product)
    return cart_count


def get_cart_total(request):
    cart_list = initialize_cart(request)
    cart_total = 0
    for product in cart_list:
        cart_total += (product.price * get_product_qty(product))
    return cart_total


def add_product_to_cart(request, product_id):
    initialize_cart(request)
    product = Product.objects.get(id=product_id)
    request.session[CART].append(product)
    request.session.save()
    return request.session[CART]


def remove_product_from_cart(request, product_id):
    cart_list_orig = initialize_cart(request)
    removed = False
    cart_list = []
    for product in cart_list_orig:
        qty = get_product_qty(product)
        if str(product.id) == str(product_id) and not removed:
            qty -= 1
            product.quantity = qty
            removed = True
        if qty > 0:
            cart_list.append(product)
    request.session[CART] = cart_list
    request.session.save()
    return cart_list


def context_app_verbose_name(request):
    return {'app_verbose_name': AppConfig.verbose_name}


def view_index(request):
    category_list = Category.objects.all()
    product_list = Product.objects.all()
    cart_list = initialize_cart(request)
    cart_count = get_cart_count(request)
    context = {
        'category_list': category_list,
        'product_list': product_list,
        'cart_list': cart_list,
        'cart_count': cart_count,
    }
    return render(request, 'index.html', context)


def view_cart(request):
    initialize_cart(request)

    if ADD in request.GET:
        product_id = request.GET.get(ADD)
        add_product_to_cart(request, product_id)
        return redirect('cart')

    if REMOVE in request.GET:
        product_id = request.GET.get(REMOVE)
        remove_product_from_cart(request, product_id)
        return redirect('cart')

    cart_total = get_cart_total(request)
    cart_list = organize_cart(request)
    cart_count = get_cart_count(request)
    context = {
        'cart_list': cart_list,
        'cart_count': cart_count,
        'cart_total': cart_total,
    }
    return render(request, 'cart.html', context)


