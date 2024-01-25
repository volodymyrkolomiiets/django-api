from rest_framework import serializers
from decimal import Decimal
from .models import MenuItem, Category
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
import bleach
#------------------------------------------------------------------------------------------------------------------
# HyperlinkedModelSerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]
        
        
class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    # title = serializers.CharField(
    #     max_length=255,
    #     validators=[UniqueValidator(queryset=MenuItem.objects.all())]
    # )
    # stock = serializers.IntegerField(source="inventory", min_value=0)
    stock = serializers.IntegerField(source="inventory")
    price_after_tax = serializers.SerializerMethodField(method_name="calculated_tax")
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ["id", "title", "price", "stock", "price_after_tax", "category", "category_id"]
        validators=[UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=["title", "price"]
            )]
        
        
        
        
        # extra_kwargs = {
        #     "title": {
        #         "validators": [UniqueValidator(
        #             queryset=MenuItem.objects.all()
        #         )]
        #     }
        # }
        
        
        # extra_kwargs = {
        #     "price": {"min_value": 2},

        # }
    def calculated_tax(self, product:MenuItem):
        return round(product.price * Decimal(1.1), 2)
    
    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError("Price should not be less than 2.0")
        
    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError("Stock cannot be negative")
    
    def validate(self, attrs):
        if attrs["price"] < 2:
            raise serializers.ValidationError("Price should not less than 2.0")
        if attrs["inventory"] < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        attrs["title"] = bleach.clean(attrs['title'])
        return super().validate(attrs)
    
    def validate_title(self, value):
        return bleach.clean(value)


#----------------------------------------------------------------------------------------------------------

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