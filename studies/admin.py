from django.urls import reverse
from django.utils.http import urlencode
from django.contrib import admin
from .models import (
    Book,
    Chapter,
    StudiesNotes,
    StudiesNotesProgression,
    UserBookMany,
    GlobalDailyAnalysis,
    GlobalMonthlyAnalysis,
)
from django.utils.html import format_html


class ChapterAdminForm(admin.TabularInline):
    model = Chapter


class NoteAdminForm(admin.TabularInline):
    model = StudiesNotes


class StudiesNotesProgressionForm(admin.TabularInline):
    model = StudiesNotesProgression


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "view_chapter_link")
    search_fields = ("name", "id", "users__email")
    inlines = [ChapterAdminForm]

    def view_chapter_link(self, obj):
        count = obj.chapter_set.count()
        url = (
            reverse("admin:studies_chapter_changelist")
            + "?"
            + urlencode({"book": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Chapter</a>', url, count)

    view_chapter_link.short_description = "Chapter"


@admin.register(UserBookMany)
class UserBookManyAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_book",
                    "book", "user_fonction", "__str__")
    search_fields = ("id",
                     "user__username")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "order_chapter",
        "book",
        "view_book_link",
        "view_notes_link",
    )
    search_fields = ("name", "id", "book__users__email")
    inlines = [NoteAdminForm]

    def view_book_link(self, obj):
        return format_html(
            '<a href="/admin/studies/book/%s/">%s</a>' % (
                obj.book.id, obj.book.name)
        )

    def view_notes_link(self, obj):
        count = obj.studiesnotes_set.count()
        url = (
            reverse("admin:studies_studiesnotes_changelist")
            + "?"
            + urlencode({"chapter": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Notes</a>', url, count)

    view_notes_link.short_description = "Notes"


@admin.register(StudiesNotes)
class StudiesNotesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order_note",
        "text_recto",
        "text_verso",
        "studie_recto",
        "studie_verso",
        "chapter",
        "view_chapter_link",
    )
    search_fields = (
        "id",
        "chapter__book__users__email",
        "chapter__book__name",
        "chapter__name",
        "text_recto",
        "text_verso",
    )
    inlines = [StudiesNotesProgressionForm]

    def view_chapter_link(self, obj):
        url = (
            reverse("admin:studies_chapter_changelist")
            + "?"
            + urlencode({"id": f"{obj.chapter.id}"})
        )
        return format_html('<a href="{}"> link</a>', url)

    view_chapter_link.short_description = "chapter"


@admin.register(StudiesNotesProgression)
class StudiesNotesProgressionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "is_recto",
        "notes",
        "level",
        "last_studied_date",
        "next_studied_date",
    )
    search_fields = (
        "id", "user__username"
    )
    list_filter = ("level",)


@admin.register(GlobalDailyAnalysis)
class GlobalDailyAnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "user",
        "date",
        "number_of_studies",
        "number_of_win",
        "number_of_lose",
    )


@admin.register(GlobalMonthlyAnalysis)
class GlobalMonthlyAnalysissAdmin(admin.ModelAdmin):
    list_display = (
        "date",
        "user",
        "date",
        "number_of_studies",
        "number_of_win",
        "number_of_lose",
    )
