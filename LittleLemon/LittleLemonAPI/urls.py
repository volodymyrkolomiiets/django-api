from django.urls import path
from . import views

urlpatterns = [
    path("menu-items", views.menu_item, name="menu-item"),
    path("menu-items/<int:pk>", views.single_menu_item, name="single-menu-item"),
    path("groups/manager/users", views.manager, name="manager"),
    path("groups/manager/users/<int:id>", views.delete_manager, name="delete-manager"),
    path("cart/menu-items", views.cart, name="cart"),
    path("orders", views.order, name="order"),
    path("orders/<int:id>", views.single_order, name="single_order"),
]
