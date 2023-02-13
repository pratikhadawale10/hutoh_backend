from django.urls import path
from address import views

urlpatterns = [
    path('', views.AddressCreateView.as_view()),
    path('<uuid:id>/',views.AddressByIDView.as_view()),
]
