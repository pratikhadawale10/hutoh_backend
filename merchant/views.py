from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from merchant.models import Merchant, Product, ProductSizeAndQuantity, ProductImage
from merchant.serializers import GetMerchantsSerializer, CreateMerchantsSerializer, GetProductsSerializer, CreateProductsSerializer
from rest_framework.response import Response
import json
import ast
class MerchantCreateView(APIView):
    permission_classes = [IsAuthenticated]
    # give his own merchant details
    def get(self,request):
        try:
            user = request.user
            queryset = Merchant.objects.get(user=user)
            serializer = GetMerchantsSerializer(queryset,context={'request': request})
            return Response({"data":serializer.data})
        except:
            return Response({"message":"Merchant Does Not Exists"})

        
    #create a new merchant
    def post(self,request):
        user = request.user
        data = request.data
        serializer = CreateMerchantsSerializer(data=data)
        if serializer.is_valid():

            if Merchant.objects.filter(user=user).exists():
                return Response({"message":"Merchant Already Exists"})

            queryset = Merchant.objects.create(
                user = user,

                shop_pic = request.FILES['shop_pic'],
                shop_name = data.get("shop_name",None),
                shop_address = data.get("shop_address",None),
                shop_description = data.get("shop_description",None),

                store_lease_document = data.get("store_lease_document",None),
                rent_bill = data.get("rent_bill",None),
                energy_bill = data.get("energy_bill",None),
                national_id_card = data.get("national_id_card",None),

                store_category = data.get("store_category",None),
                store_subcategory = data.get("store_subcategory",None),

                bank_name = data.get("bank_name",None),
                account_number = data.get("account_number",None),
                bank_address = data.get("bank_address",None),
                bvn = data.get("bvn",None),
                routing_number = data.get("routing_number",None),
            )
            queryset.save()

            serializer = GetMerchantsSerializer(queryset,context={'request': request})
            return Response({"data":serializer.data})
        else:
            return Response(serializer.errors,status=400)



class MerchantByIDView(APIView):
    permission_classes = [IsAuthenticated]
    # get merchant details by merchant id
    def get(self,request,id):
        user = request.user
        queryset = Merchant.objects.get(id=id)
        serializer = GetMerchantsSerializer(queryset,context={'request': request})
        return Response({"data":serializer.data})


class AllMerchantProfileView(APIView):
    permission_classes = [IsAuthenticated]
    # get all merchant details
    def get(self,request):
        queryset = Merchant.objects.all()
        serializer = GetMerchantsSerializer(queryset,many=True,context={'request': request})
        return Response({"data":serializer.data})
    

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    # get all products by user token
    def get(self,request):
        user = request.user
        try:
            merchant = Merchant.objects.get(user__id=user.id)
            if merchant.is_verified == False:
                return Response({"message":"Merchant is not verified"})
        except:
            return Response({"message":"Merchant Does Not Exists"})
        
        queryset = Product.objects.search_related('merchant').filter(merchant=merchant)
        serializer = GetProductsSerializer(queryset,context={'request': request},many=True)
        return Response({"data":serializer.data})


    #create a new product
    def post(self, request, format=None):
        user = request.user
        data = request.data
        serializer = CreateProductsSerializer(data=data)
        if serializer.is_valid():
            try:
                merchant = Merchant.objects.get(user__id=user.id)
                if merchant.is_verified == False:
                    return Response({"message":"Merchant is not verified"})
            except:
                return Response({"message":"Merchant Does Not Exists"})


            queryset = Product.objects.create(
                merchant = merchant,
                product_type =data.get("product_type",None),
                name =data.get("name",None),
                description =data.get("description",None),
                price =data.get("price",None),
                color =data.get("color",None),
                stock =data.get("stock",None),
            )
            images = [ProductImage.objects.create(image=image) for image in request.FILES.getlist('images')]
            queryset.images.set(images)
            queryset.save()

            for size_and_quantity in  ast.literal_eval(json.loads(json.dumps(data.get("size_and_quantity",None)))):
                product_size_and_quantity = ProductSizeAndQuantity.objects.get_or_create(
                    size = size_and_quantity["size"],
                    quantity = size_and_quantity["quantity"],
                )
                queryset.size_and_quantity.add(product_size_and_quantity[0])
                queryset.save()


            serializer = GetProductsSerializer(queryset,context={'request': request})
            return Response({"data":serializer.data})
        else:
            return Response(serializer.errors,status=400)



    
        


class ProductEditView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        user = request.user

        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)
        
        if product.merchant.user.id != user.id:
            return Response({"message": "Unauthorized request"}, status=401)
        
        serializer = GetProductsSerializer(product,context={'request': request})
        return Response({"data":serializer.data})

    def put(self, request, id):
        user = request.user
        data = request.data
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)
        
        if product.merchant.user.id != user.id:
            return Response({"message": "Unauthorized request"}, status=401)

        serializer = CreateProductsSerializer(product, data=data, partial=True)
        
        if serializer.is_valid():
            try:
                merchant = Merchant.objects.get(user__id=user.id)
                if merchant.is_verified == False:
                    return Response({"message":"Merchant is not verified"})
            except:
                return Response({"message":"Merchant does not exist"})

            product.product_type = data.get("product_type", product.product_type)
            product.name = data.get("name", product.name)
            product.description = data.get("description", product.description)
            product.price = data.get("price", product.price)
            product.color = data.get("color", product.color)
            product.stock = data.get("stock", product.stock)

            images = [ProductImage.objects.create(image=image) for image in request.FILES.getlist('images')]
            product.images.set(images)

            product.size_and_quantity.clear()
            for size_and_quantity in  ast.literal_eval(json.loads(json.dumps(data.get("size_and_quantity",None)))):
                product_size_and_quantity = ProductSizeAndQuantity.objects.get_or_create(
                    size = size_and_quantity["size"],
                    quantity = size_and_quantity["quantity"],
                )
                product.size_and_quantity.add(product_size_and_quantity[0])
            product.save()

            serializer = GetProductsSerializer(product,context={'request': request})
            return Response({"data":serializer.data})
        else:
            return Response(serializer.errors,status=400)