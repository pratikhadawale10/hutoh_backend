from rest_framework import serializers
from authentication.models import User

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password","is_superuser","is_staff","groups","user_permissions","last_login")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name","last_name")