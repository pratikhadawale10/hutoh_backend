from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from authentication.models import User
from merchant.models import Merchant
from driver.models import Driver
from merchant.serializers import GetMerchantsSerializer
from authentication.serializers import GetUserSerializer
from driver.serializers import GetDriversSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login


class UserSignUpView(APIView):
    def post(self,request):
        data = request.data

        username = data["username"]
        email = data["email"]
        phone = data["phone"]
        password = data["password"]
        # profile_pic = request.FILES['profile_pic']
        profile_pic = request.FILES.get('profile_pic')

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

        # authenticate the user and log them in to update the last_login field
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)

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

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({"status":True,
                            "refresh":str(refresh),
                            "access":str(refresh.access_token),
                            "message": "success"})
        else:
            return Response({"message":"Incorrect email or password!"})
    



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = User.objects.get(id=request.user.id)
        serializer = GetUserSerializer(queryset,context={'request': request})

        try:
            merchant_queryset = Merchant.objects.get(user__id=queryset.id)
            merchant_serializer = GetMerchantsSerializer(merchant_queryset,context={'request': request})
            merchant = merchant_serializer.data

            
        except:
            merchant = None

        try:
            driver_queryset = Driver.objects.get(user__id=queryset.id)
            driver_serializer = GetDriversSerializer(driver_queryset,context={'request': request})
            driver = driver_serializer.data
        except:
            driver = None
        
        return Response({"status":True,
                        "message": "success",
                        "data":serializer.data,
                        "merchant":merchant,
                        "driver":driver})