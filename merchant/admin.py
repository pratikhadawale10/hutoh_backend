from django.contrib import admin
from merchant.models import Merchant, ProductSizeAndQuantity, Product, ProductImage
from django.utils.html import format_html
from django.conf import settings

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail',)

    def thumbnail(self, obj):
        return format_html(
            '<div style="position:relative;width:100px;height:100px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);">'
            '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);">'
            '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
            '</div>'
            '<div style="position:absolute;top:0;left:0;width:100%;height:100%;background-color:rgba(255,255,255,0.6);opacity:0;transition:opacity 0.3s ease-out;"></div>'
            '</div>',
            obj.image.url, obj.image.url
        )

    thumbnail.short_description = 'Image'






admin.site.register(Merchant)
admin.site.register(Product)
admin.site.register(ProductSizeAndQuantity)
admin.site.register(ProductImage, ProductImageAdmin)
