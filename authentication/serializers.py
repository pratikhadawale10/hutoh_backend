from rest_framework import serializers
from authentication.models import User

class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password","is_superuser","is_staff","groups","user_permissions","last_login")