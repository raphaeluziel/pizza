from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

import time
from datetime import datetime

# Create your models here.

class Topping(models.Model):
    topping = models.CharField(max_length=64, unique=True)

    def __str__(self):
        # The top return is for older versions, like on my server
        return "{}".format(self.topping)
        #return f"{self.topping}"

class Item(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    size = models.CharField(max_length=5, null=True, blank=True)
    numExtras = models.IntegerField(default=0)
    price_extras = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    position = models.IntegerField(default=1000000)

    def __str__(self):
        # The top return is for older versions, like on my server
        return "{} {} {} for ${}".format(self.size or '', self.name, self.type, self.price)
        #return f"{self.size or ''} {self.name} {self.type} for ${self.price}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Not Submitted', 'Not Submitted'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed')
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Submitted')
    timestamp = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=200, default='Pickup')
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)

    def __str__(self):
        # The top return is for older versions, like on my server
        return "Order #{}, {} for {}.  Status: {}".format(self.id, self.timestamp.strftime('%c'), self.customer, self.status)
        #return f"Order #{self.id}, {self.timestamp.strftime('%c')} for {self.customer}.  Status: {self.status}"

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order')
    quantity = models.IntegerField(default=1)
    nameExtras = ArrayField(models.CharField(max_length=64), null=True, blank=True)
    subtotal = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        # The top return is for older versions, like on my server
        return "{} {}  each, with {} for ${}".format(self.quantity, self.item, ', '.join(self.nameExtras) or 'no addons', self.subtotal)
        #return f"{self.quantity} {self.item} each, with {', '.join(self.nameExtras) or 'no addons'} for ${self.subtotal}"
