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
class Driver(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    document_status_choices=(
        ("Pending","Pending"),
        ("Not Uploaded","Not Uploaded"),
        ("Verified","Verified"),
    )
    vehicle_type_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    fuel_type_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    other_app_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    drive_period_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    drive_reason_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
    )
    drive_time_choices=(
        ("1","1"),
        ("2","2"),
        ("3","3"),
        ("4","4"),
        ("5","5"),
        ("6","6"),
        ("7","7"),
    )

    driver_photo = models.FileField(upload_to=partial(get_upload_path, doctype="driver_photo"),null=True,blank=True)
    driver_registration = models.FileField(upload_to=partial(get_upload_path, doctype="driver_registration"),null=True,blank=True)
    insurance = models.FileField(upload_to=partial(get_upload_path, doctype="insurance"),null=True,blank=True)
    license_plate = models.FileField(upload_to=partial(get_upload_path, doctype="license_plate"),null=True,blank=True)
    safety_document = models.FileField(upload_to=partial(get_upload_path, doctype="safety_document"),null=True,blank=True)
    national_identity = models.FileField(upload_to=partial(get_upload_path, doctype="national_identity"),null=True,blank=True)

    driver_photo_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    driver_registration_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    insurance_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    license_plate_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    safety_document_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")
    national_identity_status = models.CharField(max_length=150,choices=document_status_choices,default="Pending")


    # Onboarding2
    vehicle_type = models.CharField(max_length=150,choices=vehicle_type_choices)
    year = models.IntegerField(
            validators=[MinValueValidator(1950), MaxValueValidator(2050)],
            default=2023
        )
    make = models.CharField(max_length=150)
    vehicle_class = models.CharField(max_length=150)
    fuel_type = models.CharField(max_length=150,choices=fuel_type_choices)
    color = models.CharField(max_length=150)
    number_of_door = models.CharField(max_length=150)


    # Onboarding3
    drive_reason = models.CharField(max_length=150,choices=drive_reason_choices)
    drive_period = models.CharField(max_length=150,choices=drive_period_choices)
    drive_time = models.CharField(max_length=150,choices=drive_time_choices)
    other_app = models.CharField(max_length=150,choices=other_app_choices)
    

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)