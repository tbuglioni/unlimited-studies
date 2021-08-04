from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin


class AccountAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_admin",
        "is_staff",
        "is_student",
        "is_teacher",
    )
    search_fields = (
        "email",
        "username",
    )
    readonly_fields = (
        "date_joined",
        "last_login",
    )

    filter_horizontal = ()
    list_filter = (
        "is_admin",
        "is_staff",
        "is_student",
        "is_teacher",
    )
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ("is_admin",
                                    "is_staff",
                                    "is_student",
                                    "is_teacher")}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',
                       'username',
                       'password1',
                       'password2',
                       "is_admin",
                       "is_staff",
                       "is_student",
                       "is_teacher",)}
         ),
    )


admin.site.register(Account, AccountAdmin)
