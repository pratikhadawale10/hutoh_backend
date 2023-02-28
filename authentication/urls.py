from django.urls import path
from authentication import views

urlpatterns = [
    path('singup/', views.UserSignUpView.as_view()),
    path('singin/',views.UserSignInView.as_view()),
    path('user_profile/',views.UserProfileView.as_view()),
]
