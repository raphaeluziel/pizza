from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Item, OrderItem, Order, Topping

from decimal import *

import json
import os

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import stripe

from dotenv import load_dotenv
load_dotenv()

# Create your views here.

def index(request):
    return render(request, "orders/index.html")

@login_required()
def your_orders(request):

    orders = Order.objects.filter(customer=request.user).order_by('-id')
    context = {
        "orders": orders
    }
    return render(request, "orders/your_orders.html", context)

# Return a json object of all menu items for display in the menu.html page
def menuAPI(request):
    menu = []
    for x in Item.objects.order_by('position').values():
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


@login_required()
def order(request):

    # If customer is or was working on an order, get the order
    if Order.objects.filter(customer=request.user, status='Not Submitted'):
        order = Order.objects.get(customer=request.user, status='Not Submitted')

    # Otherwise, create a new empty order
    else:
        order = Order(customer=request.user)
        order.save()

    # Get the items in the order
    items_in_order = OrderItem.objects.filter(order__id=order.id)

    # User clicks the "Add to Cart" button to add an item to the cart
    if request.method == 'POST':

        # Get item information from user
        item = Item.objects.get(pk=request.POST["item"])
        quantity = int(request.POST["quantity"])
        addons = request.POST.getlist("extras")

        # User forgot to choose correct number of toppings - send them back
        if len(addons) < item.numExtras:
            messages.error(request, "Please choose the correct number of addons for your item.")
            return HttpResponseRedirect(reverse('order'))

        # calculate price
        subtotal = (item.price + Decimal(item.price_extras * len(addons))) * quantity

        # Add the item to the customer's order
        OrderItem(item=item, order=order, quantity=quantity, nameExtras=addons, subtotal=subtotal).save()
        return HttpResponseRedirect(reverse('order'))

    context = {
        "items": Item.objects.order_by('id').all(),
        "types": Item.objects.order_by('position').distinct('position'),
        "toppings": Topping.objects.all(),
        "order_items": items_in_order or None,
        "order": order or None
        }

    return render(request, "orders/order.html", context)

@login_required()
def order_details(request, order_id):

    # Try to get see if the url get parameter matches with a real order id
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return render(request, "orders/error.html", {"message": "No order with this ID"})

    # If the logged in user requesting this is not the one who placed the order
    if order.customer != request.user:
        return render(request, "orders/error.html", {"message": "This is not a valid order number"})

    items_in_order = OrderItem.objects.filter(order__id=order.id)

    context = {
        "items_in_order": items_in_order,
        "order": order
    }
    return render(request, "orders/order_details.html", context)

@login_required()
def checkout(request):

    # If customer did not finish placing order yet
    if Order.objects.filter(customer=request.user, status='pending'):
        order = Order.objects.filter(customer=request.user, status='pending').last()
        items_in_order = OrderItem.objects.filter(order__id=order.id)
    else:
        order = {}
        items_in_order = {}

    # User clicked checkout button on the order.html file
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

        return render(request, 'orders/checkout.html', context)

        #return HttpResponseRedirect(reverse('checkout'))

    context = {
        "items_in_order": items_in_order,
        "order": order
    }

    return render(request, 'orders/checkout.html', context)


@login_required()
def confirmation(request):

    list_of_items_for_email = ''

    # User clicks Place Order order on the checkout.html file
    if request.method == "POST":

        # If all goes well, the order is submitted and marked as completed
        order = Order.objects.get(pk=request.POST['order_id'])

        stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
        token = request.POST['stripeToken']

        try:
            charge = stripe.Charge.create(
              amount=int(100 * order.total),
              currency='usd',
              description='Ralph\'s Pizza Place',
              source=token,
            )
        except:
            return render(request, 'orders/error.html', {"message": "Card Declined"})

        order.status = 'completed'
        order.save()

        items_in_order = OrderItem.objects.filter(order__id=order.id)

        for x in items_in_order:
            list_of_items_for_email = list_of_items_for_email + str(x.quantity) + " " + str(x.item) + "<br>"


        email_content = "<h1>Your Order from Ralph's Pizza is Confirmed</h1>\
                        <p>Here are your order details:</p>\
                        <p>Order ID: <b>" + str(order.id) + "</b></p>\
                        <p>" + str(list_of_items_for_email) + "</p>\
                        <p>Order Total: <b>$" + str(order.total) + "</b></p>"

        email_subject = "Order " + str(order.id) + " from pizza@raphaeluziel.net confirmed";


        # The following uses SendGrid to send a confirmation email to the user
        message = Mail(
            from_email='pizza@raphaeluziel.net',
            to_emails=request.user.email,
            subject=email_subject,
            html_content=email_content
            )
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

        return HttpResponseRedirect(reverse("confirmation"))

    return render(request, "orders/confirmation.html")


# Deletes a single item on the users cart using the delete link
def delete(request):
    OrderItem.objects.get(pk=request.POST['delete']).delete()
    return HttpResponseRedirect(reverse("order"))

# Deletes all items on the users cart using the delete button
def deleteAll(request):
    OrderItem.objects.filter(order__customer=request.user).delete()
    return HttpResponseRedirect(reverse("order"))

# Cancels an order before it is submitted
def cancel_order(request):
    Order.objects.filter(pk=request.POST['order_id']).delete()
    return HttpResponseRedirect(reverse("order"))
