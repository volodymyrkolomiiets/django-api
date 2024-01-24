from rest_framework.decorators import api_view
from .models import MenuItem, Category
from rest_framework.response import Response
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(["GET", "POST"])
def menu_item(request):
    if request.method == "GET":
        menu_items = MenuItem.objects.select_related("category").all()
        serializer_items = MenuItemSerializer(menu_items, many=True, context={'request': request})
        return Response(serializer_items.data)
    elif request.method == "POST":
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        # serialized_item.validated_data  -> access validated data
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    
        


@api_view()
def single_menu_item(request, id):
    menu_item = get_object_or_404(MenuItem, pk=id)
    serializer_item = MenuItemSerializer(menu_item, context={'request': request})
    return Response(serializer_item.data)


@api_view()
def category_detail(request, id):
    category = get_object_or_404(Category, pk=id)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)
