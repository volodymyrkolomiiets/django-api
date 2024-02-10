from .models import Category, MenuItem, Cart, Order, OrderItem
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "date_joined"]


class MenuItemField(serializers.PrimaryKeyRelatedField):
    def to_representation(self, value):
        # If value is a PKOnlyObject, fetch the actual object from the database
        if isinstance(value, serializers.PKOnlyObject):
            value = self.get_queryset().get(pk=value.pk)
        return value.title


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "category", "featured", "category_id"]

        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(), fields=["title", "price"]
            )
        ]

        extra_kwargs = {
            "price": {"min_value": 1},
            "category": {"min_value": 1, "max_value": Category.objects.count()},
        }


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemField(queryset=MenuItem.objects.all())

    class Meta:
        model = Cart
        fields = ["id", "user", "menuitem", "quantity", "unite_price", "price"]
        extra_kwargs = {
            "price": {"min_value": 1},
            "menuitem": {"min_value": 1, "max_value": MenuItem.objects.count()},
        }


class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer(read_only=True)
    menuitem_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "menuitem_id",
            "menuitem",
            "quantity",
            "unit_price",
            "price",
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_item = OrderItemSerializer(many=True, read_only=True, source="user_order")

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "delivery_crew",
            "order_item",
            "status",
            "total",
            "date",
        ]
