from django.urls import path
from merchant import views

urlpatterns = [
    path('', views.MerchantCreateView.as_view()),
    path('<uuid:id>/',views.MerchantByIDView.as_view()),
    path('all/',views.AllMerchantProfileView.as_view()),
    path('profile/',views.MerchantProfileView.as_view()),
    
    #product apis
    path('product/',views.ProductCreateView.as_view()),
    path('sample_products/',views.SampleProductsView.as_view()),
    path('product/<uuid:id>/',views.ProductEditView.as_view()),

    #cart
    path('product/cart/',views.AddToCartView.as_view()),
]
