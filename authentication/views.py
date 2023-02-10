from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.models import User

class UserSignUpView(APIView):
    def post(self,request):
        data = request.data

        username = data["username"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]

        #check if username already exists
        if User.objects.filter(username=username).exists():
            return Response({"message":"Username Already Exists"})
        #check if phone
        if User.objects.filter(phone=phone).exists():
            return Response({"message":"Phone Already Exists"})
        #check if email
        if User.objects.filter(email=email).exists():
            return Response({"message":"Email Already Exists"})


        user = User.objects.create(
            username = username,
            email = email,
            phone = phone,
        )
        user.set_password(password)
        user.save()

        return Response({"message":"User Created!"})

class UserSignInView(APIView):