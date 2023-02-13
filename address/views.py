from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from address.models import Address
from address.serializers import GetAddressSerializer, CreateAddressSerializer
from rest_framework.response import Response

class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated]
    # give list of his own addresses in return
    def get(self,request):
        user = request.user
        queryset = Address.objects.filter(user=user)
        serializer = GetAddressSerializer(queryset,many=True)
        return Response({"data":serializer.data})

    #create a new address
    def post(self,request):
        user = request.user
        data = request.data
        serializer = CreateAddressSerializer(data=data)
        if serializer.is_valid():
            queryset = Address.objects.create(
                user = user,
                address_line_1 = data.get("address_line_1",None),
                address_line_2 = data.get("address_line_2",None),
                street_name = data.get("street_name",None),
                city = data.get("city",None),
                state = data.get("state",None),
                country = data.get("country",None),
                zip = data.get("zip",None),
                location_type = data.get("location_type",None),
                house_type = data.get("house_type",None),
                floor = data.get("floor",None),
                latitude = data.get("latitude",None),
                longitude = data.get("longitude",None),
            )
            queryset.save()

            serializer = GetAddressSerializer(queryset)
            return Response({"data":serializer.data})
        else:
            return Response(serializer.errors,status=400)



class AddressByIDView(APIView):
    permission_classes = [IsAuthenticated]
    # give list of his own addresses in return
    def get(self,request,id):
        user = request.user
        queryset = Address.objects.get(id=id)
        serializer = GetAddressSerializer(queryset)
        return Response({"data":serializer.data})

    #create a new address
    def post(self,request):
        user = request.user
        data = request.data
        serializer = CreateAddressSerializer(data=data)
        if serializer.is_valid():
            queryset = Address.objects.create(
                user = user,
                address_line_1 = data.get("address_line_1",None),
                address_line_2 = data.get("address_line_2",None),
                street_name = data.get("street_name",None),
                city = data.get("city",None),
                state = data.get("state",None),
                country = data.get("country",None),
                zip = data.get("zip",None),
                location_type = data.get("location_type",None),
                house_type = data.get("house_type",None),
                floor = data.get("floor",None),
                latitude = data.get("latitude",None),
                longitude = data.get("longitude",None),
            )
            queryset.save()

            serializer = GetAddressSerializer(queryset)
            return Response({"data":serializer.data})
        else:
            return Response(serializer.errors,status=400)