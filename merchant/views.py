from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from merchant.models import Merchant
from merchant.serializers import GetMerchantsSerializer, CreateMerchantsSerializer
from rest_framework.response import Response

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
    
