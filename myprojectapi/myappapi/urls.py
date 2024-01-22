from django.urls import path
from .views import menu_item, single_item

urlpatterns = [
    path("menu-item", menu_item),
    path("menu-item/<int:id>", single_item),
]