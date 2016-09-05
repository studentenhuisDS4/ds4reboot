from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from user.models import Housemate


BaseUserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'password1', 'password2', 'first_name', 'last_name')}
    ),
)

# define an inline admin descriptor for Housemate model
class HousematInline(admin.StackedInline):
    model = Housemate
    can_delete = False
    verbose_name_plural = 'Housemate Information'
    exclude = ('sum_bier','sum_wwijn','sum_rwijn','total_bier','total_wwijn','total_rwijn',
               'boetes_open','boetes_geturfd','boetes_total','moveout_date','moveout_set')


# define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (HousematInline, )


# re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
