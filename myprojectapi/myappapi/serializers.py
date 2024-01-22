from rest_framework import serializers
from .models import MenuItem
from decimal import Decimal

# class MenuItemSerializers(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()

class MenuItemSerializers(serializers.ModelSerializer):
    stock = serializers.IntegerField(source="inventory") # 1. change the name of the field inventory to --> stock
    price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax") # 2. calculated field
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax"] # 1. after changing name include new name of the field
                                                                      # 2. add calculated field to fields list
    
    def calculated_tax(self, product:MenuItem): # 2. add calculated field
        return product.price * Decimal(1.1)