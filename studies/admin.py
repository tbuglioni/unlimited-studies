from django.contrib import admin
from .models import Book, Chapter, StudiesNotes, StudiesNotesProgression, UserBookMany


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order_book")

    search_fields = ("name",)


class UserBookManyAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "user_fonction",
                    "level_chapter", "__str__")

    search_fields = ("user", "book")


class ChapterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order_chapter", "book")

    search_fields = ("name",)


class StudiesNotesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_note",
        "text_recto",
        "text_verso",
        "studie_recto",
        "studie_verso",
        "chapter",

    )

    search_fields = ("text_recto", "text_verso")


class StudiesNotesProgressionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "notes",
        "flaged",
        "lvl_recto",
        "lvl_verso",
        "last_studied_date_recto",
        "last_studied_date_verso",
        "next_studied_date_recto",
        "next_studied_date_verso",
    )

    search_fields = ("user",)
    list_filter = (
        "flaged",
        "lvl_recto",
        "lvl_verso",
    )


admin.site.register(Book, BookAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(StudiesNotes, StudiesNotesAdmin)
admin.site.register(StudiesNotesProgression, StudiesNotesProgressionAdmin)
admin.site.register(UserBookMany, UserBookManyAdmin)
