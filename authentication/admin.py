from django.contrib import admin
from authentication.models import User
from django.contrib.auth.models import Group
from django.utils.html import format_html

class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.fields if field.name not in ['password','is_superuser','is_staff','profile_pic']]
    list_display.insert(2, 'display_profile_pic')
    def display_profile_pic(self, obj):
        if obj.profile_pic:
            border_color = 'white'
            return format_html(
                '<div style="position:relative;width:55px;height:55px;border-radius:50%;background-image:url({});background-size:cover;background-position:center;overflow:hidden;box-shadow: 0px 3px 10px rgba(0,0,0,0.2);border:2px solid {};box-sizing:border-box;">'
                '<img src="{}" style="display:block;max-width:none;width:100%;height:100%;" />'
                '</div>',
                obj.profile_pic.url, border_color, obj.profile_pic.url
            )
        else:
            return None

    display_profile_pic.short_description = 'Profile Pic'
    display_profile_pic.allow_tags = True

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
