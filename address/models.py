from django.db import models
import uuid, os, random
from authentication.models import User
from functools import partial

def get_upload_path(instance, filename, doctype):
    ext = filename.split('.')[-1]
    filename = f".{ext}"
    prefix = f"{doctype}"  # Add custom prefix
    return os.path.join("static", "address", str(instance.user.id),str(instance.hutoh_id),prefix + filename)

class Address(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hutoh_id = models.CharField(max_length=150,unique=True)
    address_id = models.CharField(max_length=150,unique=True)


    location_type_choices=(
        ("Home","Home"),
        ("Work place","Work place"),
        ("Business","Business"),
        ("Other location","Other location"),
    )
    house_type_choices=(
        ("Storey building","Storey building"),
        ("Bungalow house","Bungalow house"),
        ("Duplex with one family","Duplex with one family"),
        ("Multi family Apartment","Multi family Apartment"),
    )
    location_type = models.CharField(max_length=150,choices=location_type_choices,null=True,blank=True)
    house_type = models.CharField(max_length=150,choices=house_type_choices,null=True,blank=True)
    floor = models.CharField(max_length=150,null=True,blank=True)
    latitude = models.CharField(max_length=150,null=True,blank=True)
    longitude = models.CharField(max_length=150,null=True,blank=True)

    
    address_line_1 = models.CharField(max_length=150,null=True,blank=True)
    address_line_2 = models.CharField(max_length=150,null=True,blank=True)
    house_number = models.CharField(max_length=150,null=True,blank=True)
    street_name = models.CharField(max_length=150,null=True,blank=True)
    address_document = models.FileField(upload_to=partial(get_upload_path, doctype="address_document"),null=True,blank=True)
    phone_number = models.CharField(max_length=150,null=True,blank=True)
    fax_number = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    city = models.CharField(max_length=150,null=True,blank=True)
    state = models.CharField(max_length=150,null=True,blank=True)
    zip = models.CharField(max_length=150,null=True,blank=True)
    country = models.CharField(max_length=150,null=True,blank=True)
    

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.hutoh_id:
            self.hutoh_id = "DW" + str(random.randint(100000000000000, 999999999999999))
        if not self.address_id:
            if self.location_type=="Home":
                self.address_id = "H" + str(random.randint(1000000, 9999999))
            elif self.location_type=="Work Place":
                self.address_id = "W" + str(random.randint(1000000, 9999999))
            elif self.location_type=="Business":
                self.address_id = "B" + str(random.randint(1000000, 9999999))
            else:
                self.address_id = "L" + str(random.randint(1000000, 9999999))
        super().save(*args, **kwargs)
