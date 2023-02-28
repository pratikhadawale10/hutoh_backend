from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers import GetUserSerializer
from rest_framework.permissions import IsAuthenticated

class UserSignUpView(APIView):
    def post(self,request):
        data = request.data

        username = data["username"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        profile_pic = request.FILES['profile_pic']

        #check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({"message":"Username Already Exists"})
        #check if phone already exists
        if User.objects.filter(phone=phone).exists():
            return Response({"message":"Phone Already Exists"})
        #check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({"message":"Email Already Exists"})


        user = User.objects.create(
            username = username,
            email = email,
            phone = phone,
            profile_pic = profile_pic,
        )
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({"status":True,
                        "refresh":str(refresh),
                        "access":str(refresh.access_token),
                        "message": "success"})



class UserSignInView(APIView):
    def post(self,request):
        data = request.data

        email = data["email"]
        password = data["password"]

        try:
            user = User.objects.get(email=email)
        except:
            return Response({"message":"This email does not exists!"})

        password_check = check_password(password, user.password)
        if password_check == True:
            refresh = RefreshToken.for_user(user)
        else:
            return Response({"message":"Incorrect password!"})

        return Response({"status":True,
                        "refresh":str(refresh),
                        "access":str(refresh.access_token),
                        "message": "success"})
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = User.objects.get(id=request.user.id)
        serializer = GetUserSerializer(queryset)
        
        return Response({"status":True,
                        "message": "success",
                        "data":serializer.data})