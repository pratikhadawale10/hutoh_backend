from django.urls import path
from merchant import views

urlpatterns = [
    path('', views.MerchantCreateView.as_view()),
    path('<uuid:id>/',views.MerchantByIDView.as_view()),
    path('all/',views.AllMerchantProfileView.as_view()),
]