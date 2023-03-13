from django.contrib import admin
from merchant.models import Merchant, ProductSizeAndQuantity, Product
# Register your models here.

admin.site.register(Merchant)
admin.site.register(Product)
admin.site.register(ProductSizeAndQuantity)