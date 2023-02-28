from rest_framework import serializers
from authentication.serializers import GetUserSerializer
from address.models import Address

class GetAddressSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    class Meta:
        model = Address
        fields = "__all__"


class CreateAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("location_type","house_type","floor","latitude","longitude","address_line_1","address_line_2","house_number","street_name","phone_number","fax_number","email","city","state","zip","country",)
