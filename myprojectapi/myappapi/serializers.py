from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category

#------------------------------------------------------------------------------------------------------------------
# HyperlinkedModelSerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]
        
        
class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")

    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax", "category", "category_id"]
    
    def calculated_tax(self, product:MenuItem):
        return round(product.price * Decimal(1.1), 2)


# class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
#     stock = serializers.IntegerField(source="inventory")
#     price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")

#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name="category-detail",
#         lookup_field="id",
        
#     )
#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "stock", "price_after_tax", "category"]
    
#     def calculated_tax(self, product:MenuItem):
#         return round(product.price * Decimal(1.1), 2)


#------------------------------------------------------------------------------------------------------------------
# Create a HyperLinkedRelatedField in the serializer
#
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "slug", "title"]


# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source="inventory")
#     price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")
#     # category = serializers.StringRelatedField() 
#     category = serializers.HyperlinkedRelatedField(
#         queryset=Category.objects.all(),
#         view_name="category-detail",
#         lookup_field="id",
        
#     )
#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "stock", "price_after_tax", "category"]
    
#     def calculated_tax(self, product:MenuItem):
#         return round(product.price * Decimal(1.1), 2)


#------------------------------------------------------------------------------------------------------------------
# show related data of menu item to category add ```depth = 1````
# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source="inventory")
#     price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")

#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "stock", "price_after_tax", "category"]
#         depth = 1
        
#     def calculated_tax(self, product:MenuItem):
#         return round(product.price * Decimal(1.1), 2)

#------------------------------------------------------------------------------------------------------------------

# Display Category in Menu Item 
# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ["id", "slug", "title"]


# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source="inventory")
#     price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")
#     # category = serializers.StringRelatedField() 
#     category = CategorySerializer()
#     class Meta:
#         model = MenuItem
#         fields = ["id", "title", "price", "stock", "price_after_tax", "category"]
    
#     def calculated_tax(self, product:MenuItem):
#         return round(product.price * Decimal(1.1), 2)