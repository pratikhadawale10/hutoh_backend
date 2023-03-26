from django.contrib import admin
from merchant.models import Merchant, ProductSizeAndQuantity, Product, ProductImage
from django.utils.html import format_html, format_html_join
from django.forms.widgets import CheckboxSelectMultiple
# Register your models here.

class ProductImageCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        for i, choice in enumerate(self.choices):
            image = choice[1]
            if value and str(choice[0]) in value:
                html = format_html('<label for="{}_{}"><img src="{}" width="100"/></label>',
                                   name, i, image.image.url)
            else:
                html = format_html('<label for="{}_{}"><img src="{}" width="100"/></label>',
                                   name, i, image.image.url)
            output.append(format_html('<li><input type="checkbox" name="{}" value="{}" id="{}"{} />{}</li>',
                                      name, choice[0], '{}_{}'.format(name, i),
                                      ' checked' if value and str(choice[0]) in value else '',
                                      html))
        return format_html('<ul{}>{}</ul>', self.render_attrs(attrs), format_html_join('', '{}', output))


class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        Product.images: {'widget': ProductImageCheckboxSelectMultiple},
    }

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'id', 'created_at', 'updated_at')



admin.site.register(Merchant)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizeAndQuantity)
admin.site.register(ProductImage, ProductImageAdmin)
