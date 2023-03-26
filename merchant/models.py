from django.db import models
import uuid, os
from django.core.validators import MinValueValidator, MaxValueValidator
from functools import partial
from authentication.models import User
import uuid, os, random
from django.utils.html import format_html

def get_upload_path(instance, filename, doctype):
    ext = filename.split('.')[-1]
    filename = f".{ext}"
    prefix = f"{doctype}"  # Add custom prefix
    return os.path.join("static", "driver", str(instance.user.id), prefix + filename)

# Create your models here.
class Merchant(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    status_choices=(
        ("Pending","Pending"),
        ("Not Uploaded","Not Uploaded"),
        ("Verified","Verified"),
    )
    store_category_choices=(
        ("Fashion","Fashion"),
        ("Spare Parts","Spare Parts"),
        ("Mobile Phones","Mobile Phones"),
        ("Grocery","Grocery"),
        ("Computer Store","Computer Store"),
    )
    store_subcategory_choices=(
        ("Tshirts","Tshirts"),
        ("Wollen Sweater","Wollen Sweater"),
        ("Blazers","Blazers"),
        ("Socks","Socks"),
        ("Jeans","Jeans"),
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

    store_lease_document_status = models.CharField(max_length=150,choices=status_choices,default="Pending")
    rent_bill_status = models.CharField(max_length=150,choices=status_choices,default="Pending")
    energy_bill_status = models.CharField(max_length=150,choices=status_choices,default="Pending")
    national_id_card_status = models.CharField(max_length=150,choices=status_choices,default="Pending")


    # Onboarding3
    store_category = models.CharField(max_length=150,choices=store_category_choices)
    store_subcategory = models.CharField(max_length=150,choices=store_subcategory_choices)



    # Onboarding4
    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=150)
    bank_address = models.CharField(max_length=150)
    bvn = models.CharField(max_length=150,null=True,blank=True)
    routing_number = models.CharField(max_length=150,null=True,blank=True)

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)



class ProductSizeAndQuantity(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    size = models.CharField(max_length=150,null=True,blank=True)
    quantity = models.CharField(max_length=150,null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)



class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='static/product_images')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def thumbnail(self):
        return format_html('<img src="{}" width="50" height="50" />'.format(self.image.url))

    thumbnail.short_description = 'Image'

    def __str__(self):
        return self.image.url


class Product(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    merchant = models.ForeignKey(Merchant,on_delete=models.CASCADE)
    images = models.ManyToManyField(ProductImage)
    product_category_choices=(
        ("Shirt","Shirt"),
        ("Sweat Shirt","Sweat Shirt"),
    )
    product_type = models.CharField(max_length=150,choices=product_category_choices,null=True,blank=True)
    
    name = models.CharField(max_length=150,null=True,blank=True)
    description = models.CharField(max_length=150,null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    size_and_quantity = models.ManyToManyField(ProductSizeAndQuantity)

    product_color_choices = (
    ("Red", "Red"),
    ("Blue", "Blue"),
    ("Green", "Green"),
    ("Yellow", "Yellow"),
    ("Purple", "Purple"),
    ("Orange", "Orange"),
    ("Pink", "Pink"),
    ("Black", "Black"),
    ("White", "White"),
    ("Gray", "Gray"),
    ("Brown", "Brown"),
    ("Beige", "Beige"),
    ("Navy", "Navy"),
    ("Teal", "Teal"),
    ("Magenta", "Magenta"),
    ("Turquoise", "Turquoise"),
    ("Olive", "Olive"),
    ("Lime", "Lime"),
    ("Gold", "Gold"),
    ("Silver", "Silver"),
    ("Bronze", "Bronze"),
    )
    color = models.CharField(max_length=150,choices=product_color_choices,null=True,blank=True)

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def get_images_urls(self):
        return "\n".join([image.image.url for image in self.images.all()])



    
