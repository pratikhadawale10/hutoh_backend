from django.db import models
import uuid
import random
from authentication.models import User

class Address(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hutoh_id = models.CharField(max_length=150,unique=True,null=True,blank=True)
    address_id = models.CharField(max_length=150,unique=True,null=True,blank=True)
    address_line_1 = models.CharField(max_length=150)
    address_line_2 = models.CharField(max_length=150)
    street_name = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    zip = models.CharField(max_length=150)
    location_type_choices=(
        ("Home","Home"),
        ("Work Place","Work Place"),
        ("Business","Business"),
        ("Other Location","Other Location"),
    )
    location_type = models.CharField(max_length=150,choices=location_type_choices)
    house_type = models.CharField(max_length=150)
    floor = models.CharField(max_length=150)
    latitude = models.CharField(max_length=150)
    longitude = models.CharField(max_length=150)
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
