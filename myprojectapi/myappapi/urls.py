from django.urls import path
from . import views

urlpatterns = [
    path("menu-items", views.menu_item, name="menuitem"),
    path("menu-items/<int:id>", views.single_menu_item, name="menuitem-detail"),
    path("category/<int:id>", views.category_detail, name="category-detail"),
    path("menu", views.menu),
    path("welcome", views.welcome),
    path("csv-menu-items", views.csv_menu_items),
    path("yaml-menu-items", views.yaml_menu_items),
    path("menu-items-sets", views.MenuItemsViewSet.as_view({"get": "list", "post": "create"})),
    path("menu-items-sets/<int:pk>", views.MenuItemsViewSet.as_view({"get": "retrieve"}))
    
]