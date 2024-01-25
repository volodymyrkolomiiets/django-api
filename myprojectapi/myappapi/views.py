from rest_framework.decorators import api_view, renderer_classes
from .models import MenuItem, Category
from rest_framework.response import Response
from .serializers import MenuItemSerializer, CategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework_csv.renderers import CSVRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import viewsets





@api_view(["GET", "POST"])
def menu_item(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related("category").all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get("to_price")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")
        
        perpage = request.query_params.get("perpage", default=2)
        page = request.query_params.get("page", default=1)
        
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__istartswith=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
            
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serializer_items = MenuItemSerializer(items, many=True, context={'request': request})
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

@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related("category").all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({"data": serialized_item.data}, template_name="menu-item.html")

@api_view(["GET"])
@renderer_classes([StaticHTMLRenderer])
def welcome(request):
    data = "<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>"
    return Response(data)

@api_view()
# @renderer_classes([CSVRenderer])
def csv_menu_items(request):
    menu_items = MenuItem.objects.select_related("category").all()
    serializer_items = MenuItemSerializer(menu_items, many=True, context={'request': request})
    return Response(serializer_items.data)

@api_view()
# @renderer_classes([YAMLRenderer])
def yaml_menu_items(request):
    menu_items = MenuItem.objects.select_related("category").all()
    serializer_items = MenuItemSerializer(menu_items, many=True, context={'request': request})
    return Response(serializer_items.data)


class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fileds = ["price", "inventory"]
    search_fields = ["title", "category__title"]
