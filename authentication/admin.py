from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Lab
from django.utils.translation import ugettext_lazy as _



admin.site.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_labs',)

    def get_labs(self, obj):
        # for the many to many case labs = "\n".join([p.lab_name for p in obj.labs.all()])
        labs = ""
        if obj.lab is not None:
            labs = obj.lab.lab_name
        return labs

    get_labs.short_description = "Lab"
    fieldsets = (
            (None, {'fields': ('email',)}),
            (_('Personal info'), {'fields': ('first_name', 'last_name')}),
            (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                           'groups', 'user_permissions', 'lab')}),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )



@admin.register(Lab)
class LabAdmin(admin.ModelAdmin):
    list_display = ('lab_name', 'active', 'created')
    readonly_fields = ['created']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
