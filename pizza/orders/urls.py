from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order", views.order, name="order"),
    path("order_details/<int:order_id>", views.order_details, name="order_details"),
    path("confirmation", views.confirmation, name="confirmation"),
    path("checkout", views.checkout, name="checkout"),
    path("menu", views.menu, name="menu"),
    path("menuAPI", views.menuAPI, name="menuAPI"),
    path("toppingsAPI", views.toppingsAPI, name="toppingsAPI"),
    path("delete", views.delete, name="delete"),
    path("deleteAll", views.deleteAll, name="deleteAll"),
    path("cancel_order", views.cancel_order, name="cancel_order"),
    path("your_orders", views.your_orders, name="your_orders")
]
