from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import MenuItem
from .serializers import MenuItemSerializers
from django.shortcuts import get_object_or_404

# @api_view( )
# def menu_item(request):
#     items = MenuItem.objects.all()
#     return Response(items.values())


@api_view()
def menu_item(request):
    items = MenuItem.objects.all()
    serializerd_item = MenuItemSerializers(items, many=True)
    return Response(serializerd_item.data)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializers(item)
    return Response(serialized_item.data)
