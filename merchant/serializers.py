from rest_framework import serializers
from authentication.serializers import GetUserSerializer
from merchant.models import Merchant, Product, ProductImage, ProductSizeAndQuantity, Cart
class GetMerchantsSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    class Meta:
        model = Merchant
        fields = "__all__"


class CreateMerchantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ("shop_pic","shop_name","shop_address","shop_description","store_lease_document","rent_bill","energy_bill","national_id_card","store_category","store_subcategory","bank_name","account_number","bank_address","bvn","routing_number",)


class GetSizeAndQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSizeAndQuantity
        fields = ('size', 'quantity',)

class GetImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"

class GetProductsSerializer(serializers.ModelSerializer):
    merchant = GetMerchantsSerializer()
    size_and_quantity = GetSizeAndQuantitySerializer(many=True)
    images = GetImagesSerializer(many=True)
    class Meta:
        model = Product
        fields = "__all__"


class CreateProductsSerializer(serializers.ModelSerializer):
    size_and_quantity = serializers.CharField()
    images = serializers.ImageField()
    class Meta:
        model = Product
        fields = ("product_type", "name", "description", "price", "size_and_quantity", "color", "stock","images")



class GetCartSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    product = GetProductsSerializer()
    class Meta:
        model = Cart
        fields = "__all__"



class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("product_id", "quantity")






# #gpt
# class ProductSizeAndQuantitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductSizeAndQuantity
#         fields = ('id', 'name', 'quantity', 'created_at', 'updated_at')


# class ProductImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductImage
#         fields = ('id', 'image', 'created_at', 'updated_at')
#         read_only_fields = ('created_at', 'updated_at')


# class ProductSerializer(serializers.ModelSerializer):
#     merchant = serializers.PrimaryKeyRelatedField(queryset=Merchant.objects.all(), required=False)
#     size_and_quantity = ProductSizeAndQuantitySerializer(many=True)
#     images = serializers.ListField(child=serializers.ImageField(), required=True)  # Update the images field

#     class Meta:
#         model = Product
#         fields = (
#             'id', 'merchant', 'product_type', 'name', 'description', 'price',
#             'stock', 'color', 'size_and_quantity', 'images', 'created_at', 'updated_at'
#         )
#         read_only_fields = ('created_at', 'updated_at')

#     def create(self, validated_data):
#         size_and_quantity_data = validated_data.pop('size_and_quantity')
#         images_data = self.context['request'].FILES.getlist('images')

#         # images_data = self.validated_data.pop('images')  # Get the images data from validated_data
#         product = Product.objects.create(**validated_data)
        
#         size_and_quantitity = [ProductSizeAndQuantity.objects.create(product=product, **size_and_quantity) for size_and_quantity in size_and_quantity_data]
#         images = [ProductImage.objects.create(image=image) for image in images_data]

#         product.images.set(images)
#         product.size_and_quantity.set(size_and_quantitity)
#         product.save()
#         return product



