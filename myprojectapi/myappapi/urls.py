from django.urls import path
from . import views

urlpatterns = [
    path("menu-item", views.menu_item, name="menuitem"),
    path("menu-item/<int:id>", views.single_menu_item, name="menuitem-detail"),
    path("category/<int:id>", views.category_detail, name="category-detail")
    
]