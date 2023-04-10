from django.contrib import admin
from address.models import Address
from django.utils.html import format_html

class AddressAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Address._meta.fields  if field.name not in ["address_document"]]

    list_display.insert(2, 'display_address_document')
    def display_address_document(self, obj):
        if obj.address_document:
            if obj.is_verified == True:
                border_color = 'green'
            else:
                border_color = 'red'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.address_document.url, border_color, obj.address_document.url
            )
        else:
            return None

    display_address_document.short_description = 'Address Document'
    display_address_document.allow_tags = True

admin.site.register(Address, AddressAdmin)




