from django.db import models
import uuid, os
from django.core.validators import MinValueValidator, MaxValueValidator
from functools import partial
from authentication.models import User

def get_upload_path(instance, filename, doctype):
    ext = filename.split('.')[-1]
    filename = f".{ext}"
    prefix = f"{doctype}"  # Add custom prefix
    return os.path.join("static", "driver", str(instance.user.id), prefix + filename)

# Create your models here.
class Merchant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    document_status_choices=(
        ("Pending","Pending"),
        ("Not Uploaded","Not Uploaded"),
        ("Verified","Verified"),
    )
    store_category_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    store_subcategory_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )

    # Onboarding1
    shop_pic = models.FileField(upload_to=partial(get_upload_path, doctype="shop_pic"),null=True,blank=True)
    shop_name = models.CharField(max_length=150)
    shop_address = models.CharField(max_length=250)
    shop_description = models.TextField()


    # Onboarding2
    store_lease_document = models.FileField(upload_to=partial(get_upload_path, doctype="store_lease_document"),null=True,blank=True)
    rent_bill = models.FileField(upload_to=partial(get_upload_path, doctype="rent_bill"),null=True,blank=True)
    energy_bill = models.FileField(upload_to=partial(get_upload_path, doctype="energy_bill"),null=True,blank=True)
    national_id_card = models.FileField(upload_to=partial(get_upload_path, doctype="national_id_card"),null=True,blank=True)

    store_lease_document = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    rent_bill = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    energy_bill = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    national_id_card = models.CharField(max_length=150,choices=document_status_choices,default="Pending")


    # Onboarding3
    store_category = models.CharField(max_length=150,choices=store_category_choices)
    store_subcategory = models.CharField(max_length=150,choices=store_subcategory_choices)



    # Onboarding4
    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=150)
    bank_address = models.CharField(max_length=150)
    bvn = models.CharField(max_length=150,null=True,blank=True)
    routing_number = models.CharField(max_length=150,null=True,blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)