from rest_framework import serializers
from authentication.serializers import GetUserSerializer
from merchant.models import Merchant

class GetMerchantsSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    class Meta:
        model = Merchant
        fields = "__all__"


class CreateMerchantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ("shop_pic","shop_name","shop_address","shop_description","store_lease_document","rent_bill","energy_bill","national_id_card","store_category","store_subcategory","bank_name","account_number","bank_address","bvn","routing_number",)
