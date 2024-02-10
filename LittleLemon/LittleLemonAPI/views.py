from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import MenuItem, Cart, Order
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from . import serializers
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import MenuItemSerializer
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from .utils import CustomPageNumberPagination


# Create your views here.
@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def menu_item(request):
    if request.method == "GET":
        items = MenuItem.objects.all()
        category_name = request.query_params.get("category")
        to_price = request.query_params.get("category")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")

        perpage = request.query_params.get("perpage", default=4)
        page = request.query_params.get("page", default=1)

        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lth=to_price)
        if search:
            items = items.filter(title_istartswith=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = CustomPageNumberPagination()

        paginated_items = paginator.paginate_queryset(items, request)

        # paginator = Paginator(items, per_page=perpage)
        # try:
        #     items = paginator.page(number=page)
        # except EmptyPage:
        #     items = []

        serializer_items = serializers.MenuItemSerializer(
            paginated_items, many=True, context={"request", request}
        )
        # return Response(serializer_items.data, status.HTTP_200_OK)
        return paginator.get_paginated_response(serializer_items.data)
    elif request.method == "POST":
        managers_group = Group.objects.get(name="Manager")
        if managers_group not in request.user.groups.all():
            return Response(
                {"error": "Permission denied. Managers only"}, status.HTTP_403_FORBIDDEN
            )
        serializer_item = MenuItemSerializer(data=request.data)
        serializer_item.is_valid(raise_exception=True)
        serializer_item.save()
        return Response(serializer_item.data, status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def single_menu_item(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == "GET":
        serializer_item = MenuItemSerializer(item)
        return Response(serializer_item.data, status.HTTP_200_OK)
    managers_group = Group.objects.get(name="Manager")
    if managers_group in request.user.groups.all():

        if request.method in ["PUT", "PATCH"]:
            serializer_item = MenuItemSerializer(
                item, data=request.data, partial=request.method == "PATCH"
            )
            serializer_item.is_valid(raise_exception=True)
            serializer_item.save()
            return Response(serializer_item.data, status.HTTP_200_OK)
        if request.method == "DELETE":
            item.delete()
            return Response(status.HTTP_204_NO_CONTENT)
    return Response(
        {"error": "permission denied. Managers only"}, status.HTTP_403_FORBIDDEN
    )


@api_view(["POST", "GET"])
@permission_classes([IsAdminUser])
def manager(request):
    if request.method == "GET":
        manager_users = User.objects.filter(groups__name="Manager")
        serializer_user = serializers.UserSerializer(manager_users, many=True)
        return Response(serializer_user.data, status.HTTP_200_OK)

    username = request.data["username"]
    if not username:
        return Response({"message": "User does not exist"}, status.HTTP_404_NOT_FOUND)

    user = get_object_or_404(User, username=username)
    managers = Group.objects.get(name="Manager")
    if request.method == "POST":
        managers.user_set.add(user)
    return Response(
        {"message": f"User {username} was added to the Managers group"},
        status.HTTP_201_CREATED,
    )


@api_view(["DELETE"])
@permission_classes([IsAdminUser])
def delete_manager(request, id):
    user = get_object_or_404(User, pk=id)
    if not user.groups.filter(name="Manager").exists():
        return Response(
            {"message": f"User with {id} is not in the Manager group"},
            status.HTTP_404_NOT_FOUND,
        )
    managers = Group.objects.get(name="Manager")
    managers.user_set.remove(user)
    return Response({"message": f"User with {id} was removed from the Manager group"})


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def cart(request):
    if request.method == "GET":
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(status.HTTP_204_NO_CONTENT)
        cart_serializer = serializers.CartSerializer(cart)
        return Response(cart_serializer.data, status.HTTP_200_OK)
    elif request.method == "POST":

        menuitem_id = request.data.get("menuitem_id")
        quantity = request.data.get("quantity")

        try:
            menuitem = MenuItem.objects.get(pk=menuitem_id)
        except MenuItem.DoesNotExist:
            return Response({"error": "Menu item not found"}, status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:

            cart_data = {
                "user": request.user.id,
                "menuitem": menuitem.id,
                "quantity": quantity,
                "unite_price": menuitem.price,
                "price": menuitem.price * int(quantity),
            }

            cart_serializer = serializers.CartSerializer(data=cart_data)
            cart_serializer.is_valid(raise_exception=True)
            cart_serializer.save()
            return Response(cart_serializer.data, status.HTTP_201_CREATED)

        if cart.menuitem.id == menuitem.id:
            total_quantity = cart.quantity + int(quantity)

            data = {
                "price": menuitem.price * total_quantity,
                "quantity": total_quantity,
            }

            cart_serializer = serializers.CartSerializer(cart, data=data, partial=True)
            cart_serializer.is_valid(raise_exception=True)
            cart_serializer.save()

            return Response(cart_serializer.data, status.HTTP_200_OK)
        else:
            return Response(
                {"error": f"Close the cart with the {cart.menuitem.title}"},
                status.HTTP_400_BAD_REQUEST,
            )

    elif request.method == "DELETE":
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(status.HTTP_204_NO_CONTENT)

        cart.delete()
        return Response({"message": "your cart was removed"}, status.HTTP_200_OK)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def order(request):
    if request.method == "GET":
        managers_group = Group.objects.get(name="Manager")

        if managers_group in request.user.groups.all():
            order = Order.objects.filter(status=0)

        elif Group.objects.get(name="delivery_crew") in request.user.groups.all():
            order = Order.objects.filter(status=0, delivery_crew=request.user.id)

        else:
            order = Order.objects.filter(status=0, user=request.user)

        order_serializer = serializers.OrderSerializer(order, many=True)
        return Response(order_serializer.data)

    elif request.method == "POST":
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {"error": f"User {request.user.username} has empty cart"},
                status.HTTP_204_NO_CONTENT,
            )

        order_data = {
            "user": request.user.id,
            "total": cart.price,
            "date": datetime.now().date(),
        }

        order_serializer = serializers.OrderSerializer(data=order_data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()

        order_item_data = {
            "order": order_serializer.data["id"],
            "menuitem_id": cart.menuitem.id,
            "quantity": cart.quantity,
            "unit_price": cart.unite_price,
            "price": cart.price,
        }

        menuitem_serializer = serializers.OrderItemSerializer(data=order_item_data)
        menuitem_serializer.is_valid(raise_exception=True)
        menuitem_serializer.save()
        cart.delete()
        return Response(menuitem_serializer.data, status.HTTP_201_CREATED)


@api_view(["PUT", "PATCH", "GET", "DELETE"])
@permission_classes([IsAuthenticated])
def single_order(request, id):
    try:
        order = Order.objects.get(pk=id)

    except Order.DoesNotExist:
        return Response({"err": f"order with {id} does not exist!"})

    managers_group = Group.objects.get(name="Manager")

    if managers_group in request.user.groups.all():
        if request.method in ["PUT", "PATCH"]:
            order_serializer = serializers.OrderSerializer(
                order, data=request.data, partial=request.method == "PATCH"
            )
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
            return Response(order_serializer.data, status.HTTP_200_OK)
        elif request.method == "DELETE":
            order.delete()
            return Response(status.HTTP_204_NO_CONTENT)
        else:
            order_serializer = serializers.OrderSerializer(order)
            return Response(order_serializer.data)
    delivery_crew = Group.objects.get(name="delivery_crew")
    if request.method == "PATCH" and delivery_crew in request.user.groups.all():
        if request.user.id != order.delivery_crew.id:
            return Response(
                {
                    "err": f"order for user {request.user.username.title()} does not exists"
                },
                status.HTTP_400_BAD_REQUEST,
            )

        order_serializer = serializers.OrderSerializer(
            order, data={"status": 1}, partial=True
        )
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response(order_serializer.data, status.HTTP_200_OK)

    elif request.method == "GET":
        if request.user.id != order.user.id:
            return Response(
                {
                    "err from regular user": f"order for user {request.user.username.title()} does not exists"
                },
                status.HTTP_400_BAD_REQUEST,
            )
        order_serializer = serializers.OrderSerializer(order)
        return Response(order_serializer.data)
