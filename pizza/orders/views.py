from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from django.contrib.auth.models import User

from .models import Item, OrderItem, Order, Topping

from decimal import *

import json

# Create your views here.

def index(request):
    orders = Order.objects.filter(customer=request.user)
    context = {
        "orders": orders
    }
    return render(request, "orders/index.html", context)

# Return a json object of all menu items for display in the menu.html page
def menuAPI(request):
    menu = []
    for x in Item.objects.values():
        menu.append(x)
    menuJSON = JsonResponse(menu, safe=False)
    return HttpResponse(menuJSON)

# Return a json object of all the toppings for display in the menu page
def toppingsAPI(request):
    toppings = []
    for x in Topping.objects.values():
        toppings.append(x)
    toppingsJSON = JsonResponse(toppings, safe=False)
    return HttpResponse(toppingsJSON)

# Since all the work is done by the menu.js file requesting the lists of
# items from the API's above, all the menu route has to do is go to the
# menu.html page
def menu(request):
    return render(request, "orders/menu.html")

def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            return render(request, "orders/index.html")
        else:
            return render(request, "orders/login.html")


def order(request):

    # If customer gets here without logging in, send them to log in page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # If customer is or was working on an order, get the order
    elif Order.objects.filter(customer=request.user, status='Not Submitted'):
        order = Order.objects.get(customer=request.user, status='Not Submitted')

    # Otherwise, create a new empty order
    else:
        order = Order(customer=request.user)
        order.save()

    # Get the items in the order
    items_in_order = OrderItem.objects.filter(order__id=order.id)

    # User clicks the "Add to Cart" button to add an item to the cart
    if request.method == 'POST':
        item = Item.objects.get(pk=request.POST["item"])
        quantity = int(request.POST["quantity"])
        subtotal = item.price * quantity

        addons = request.POST.getlist("extras")
        if len(addons) < item.numExtras:
            messages.error(request, "Please choose the correct number of addons for your item.")
            return HttpResponseRedirect(reverse('order'))

        # Extras for subs are $0.50.  This is hardcoded - NEED TO CHANGE!!!
        if item.type == 'Sub':
            subtotal = subtotal + Decimal(0.50 * len(addons))

        # Add the item to the customer's order
        OrderItem(item=item, order=order, quantity=quantity, nameExtras=addons, subtotal=subtotal).save()
        return HttpResponseRedirect(reverse('order'))

    context = {
        "items": Item.objects.all(),
        "types": Item.objects.values('type').distinct(),
        "toppings": Topping.objects.all(),
        "order_items": items_in_order or None,
        "order": order or None
        }

    return render(request, "orders/order.html", context)

def order_details(request, order_id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No order with this ID"})

    if order.customer != request.user:
        return render(request, "orders/error.html", {"message": "This is not a valid order number"})

    items_in_order = OrderItem.objects.filter(order__id=order.id)

    context = {
        "items_in_order": items_in_order,
        "order": order
    }
    return render(request, "orders/order_details.html", context)


def confirmation(request):

    # If user is not logged in, send user to login page
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    # User submits order on the order.html file
    if request.method == "POST":
        order_id = request.POST["order_id"]

        # Get the order and the items in the order
        order = Order.objects.get(pk=order_id)
        items_in_order = OrderItem.objects.filter(order__id=order.id)
        if not items_in_order:
            return HttpResponseRedirect(reverse('order'))

        # Calculate the total proce of all the items in the order
        total = 0
        for x in OrderItem.objects.filter(order__id=order_id):
            total = total + x.subtotal

        # Update the order, ande save it
        order.total = total
        order.status = 'pending'
        order.save()

        context = {
            "items_in_order": items_in_order,
            "order": order
        }

        return render(request, "orders/confirmation.html", context)

    else:
        return render(request, "orders/error.html")



def delete(request):
    OrderItem.objects.get(pk=request.POST['delete']).delete()
    return HttpResponseRedirect(reverse("order"))

def deleteAll(request):
    OrderItem.objects.filter(order__customer=request.user).delete()
    return HttpResponseRedirect(reverse("order"))
