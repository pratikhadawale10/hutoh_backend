from rest_framework import serializers
from authentication.serializers import GetUserSerializer
from driver.models import Driver

class GetDriversSerializer(serializers.ModelSerializer):
    user = GetUserSerializer()
    class Meta:
        model = Driver
        fields = "__all__"

