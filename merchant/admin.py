from django.contrib import admin
from merchant.models import Merchant, ProductSizeAndQuantity, Product, ProductImage, Cart
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





class MerchantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Merchant._meta.fields if field.name not in ["shop_pic","store_lease_document","rent_bill","energy_bill","national_id_card","store_lease_document_status","rent_bill_status","energy_bill_status","national_id_card_status"]]
    list_display.insert(2, 'display_shop_pic')
    list_display.insert(6, 'display_store_lease_document')
    list_display.insert(7, 'display_rent_bill')
    list_display.insert(8, 'display_energy_bill')
    list_display.insert(9, 'display_national_id_card')
    def display_shop_pic(self, obj):
        if obj.shop_pic:
            border_color = 'green' if obj.is_verified else 'red'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.shop_pic.url, border_color, obj.shop_pic.url
            )
        else:
            return None

    display_shop_pic.short_description = 'Shop Pic'
    display_shop_pic.allow_tags = True


    def display_store_lease_document(self, obj):
        if obj.store_lease_document:
            store_lease_document_status = obj.store_lease_document_status
            if store_lease_document_status == 'Pending':
                border_color = 'yellow'
            elif store_lease_document_status == 'Not Uploaded':
                border_color = 'red'
            else:
                border_color = 'green'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.store_lease_document.url, border_color, obj.store_lease_document.url
            )
        else:
            return None

    display_store_lease_document.short_description = 'store lease document'
    display_store_lease_document.allow_tags = True

    def display_rent_bill(self, obj):
        if obj.rent_bill:
            rent_bill_status = obj.rent_bill_status
            if rent_bill_status == 'Pending':
                border_color = 'yellow'
            elif rent_bill_status == 'Not Uploaded':
                border_color = 'red'
            else:
                border_color = 'green'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.rent_bill.url, border_color, obj.rent_bill.url
            )
        else:
            return None

    display_rent_bill.short_description = 'rent bill'
    display_rent_bill.allow_tags = True


    def display_energy_bill(self, obj):
        if obj.energy_bill:
            energy_bill_status = obj.energy_bill_status
            if energy_bill_status == 'Pending':
                border_color = 'yellow'
            elif energy_bill_status == 'Not Uploaded':
                border_color = 'red'
            else:
                border_color = 'green'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.energy_bill.url, border_color, obj.energy_bill.url
            )
        else:
            return None

    display_energy_bill.short_description = 'energy bill'
    display_energy_bill.allow_tags = True


    def display_national_id_card(self, obj):
        if obj.national_id_card:
            national_id_card_status = obj.national_id_card_status
            if national_id_card_status == 'Pending':
                border_color = 'yellow'
            elif national_id_card_status == 'Not Uploaded':
                border_color = 'red'
            else:
                border_color = 'green'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.national_id_card.url, border_color, obj.national_id_card.url
            )
        else:
            return None

    display_national_id_card.short_description = 'national id card'
    display_national_id_card.allow_tags = True




class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields if field.name not in ["merchant"]]
    list_display.insert(4, 'display_images')
    list_display.insert(1, 'merchant_info')

    def merchant_info(self, obj):
        merchant = obj.merchant
        if merchant:
            border_color = 'green' if merchant.is_verified else 'red'
            return format_html('<div style="display:flex;"><div style="flex:1;margin:5px;"><div style="position:relative;width:100%;height:100%;border-radius:50%;background-image:url({shop_pic_url});background-size:cover;background-position:center;overflow:hidden;box-shadow:0px 3px 10px rgba(0,0,0,0.2);border: 2px solid {border_color}"><img src="{shop_pic_url}" style="display:block;max-width:none;width:55px;height:55px;"></div></div><div style="flex:1;margin:5px;line-height:55px;">{username}</div></div>'.format(
                shop_pic_url=merchant.shop_pic.url if merchant.shop_pic else '',
                username=merchant.user.username if merchant.user else '',
                border_color=border_color
            ))
        else:
            return '-'

    merchant_info.short_description = 'Merchant'


    def display_images(self, obj):
        images = obj.images.all()
        image_count = len(images)
        rows = (image_count - 1) // 3 + 1
        html = ''
        for i in range(rows):
            html += '<div style="display:flex;">'
            for j in range(3):
                index = i*3+j
                if index < image_count:
                    image = images[index]
                    html += '<div style="flex:1;margin:5px;"><div style="position:relative;width:100%;height:100%;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow:0px 3px 10px rgba(0,0,0,0.2);"><img src="{}" style="display:block;max-width:none;width:55px;height:55px;"></div></div>'.format(image.image.url, image.image.url)
                elif image_count % 3 == 2 and index == image_count:
                    html += '<div style="flex:1;margin:5px;"></div>'
            html += '</div>'
        return format_html(html)

    display_images.short_description = 'Images'
    display_images.allow_tags = True




class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields if field.name not in []]





class ProductSizeAndQuantityAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductSizeAndQuantity._meta.fields if field.name not in []]


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizeAndQuantity, ProductSizeAndQuantityAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ProductImage, ProductImageAdmin)