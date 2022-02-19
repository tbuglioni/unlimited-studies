from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account
from studies.models import Book


class ChapterBookForm(admin.TabularInline):
    model = Book.users.through


@admin.register(Account)
class AccountAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "username",
        "date_joined",
        "last_login",
        "view_books_link",
        "is_admin",
        "is_staff",
        "is_student",
        "is_teacher",
    )

    @staticmethod
    def view_books_link(obj):
        count = obj.books.count()
        url = (
            reverse("admin:studies_book_changelist")
            + "?"
            + urlencode({"users": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} link(s)</a>', url, count)

    view_books_link.short_description = "books"

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
        (None, {"fields": ("email", "username", "password")}),
        (
            "Permissions",
            {"fields": ("is_admin", "is_staff", "is_student", "is_teacher")},
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_admin",
                    "is_staff",
                    "is_student",
                    "is_teacher",
                ),
            },
        ),
    )
    inlines = [ChapterBookForm]
