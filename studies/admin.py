from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import (Book, Chapter, GlobalDailyAnalysis, GlobalMonthlyAnalysis,
                     StudiesNotes, StudiesNotesProgression, UserBookMany)


class ChapterAdminForm(admin.TabularInline):
    model = Chapter
    extra = 0 # how many extra forms should be displayed


class NoteAdminForm(admin.TabularInline):
    model = StudiesNotes
    extra = 0


class StudiesNotesProgressionForm(admin.TabularInline):
    model = StudiesNotesProgression
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "view_chapter_link")
    search_fields = ("name", "id", "users__email")
    inlines = [ChapterAdminForm]

    @staticmethod
    def view_chapter_link(obj):
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
    autocomplete_fields = ("user", "book")
    list_display = ("id", "user", "order_book",
                    "book", "user_fonction", "__str__")
    search_fields = ("id",
                     "user__email")


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    autocomplete_fields = ("book",) #add search bar in field book linked to book search_field
    list_display = (
        "id",
        "name",
        "order_chapter",
        "book",
        "view_book_link",
        "view_notes_link",
    )
    
    list_select_related = ['book']
    search_fields = ("name", "id", "book__users__email")
    inlines = [NoteAdminForm]

    @staticmethod
    def view_book_link(obj):
        return format_html(
            '<a href="/admin/studies/book/%s/">%s</a>' % (
                obj.book.id, obj.book.name)
        )

    @staticmethod
    def view_notes_link(obj):
        count = obj.studiesnotes_set.count()
        url = (
            reverse("admin:studies_studiesnotes_changelist")
            + "?"
            + urlencode({"chapter": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Notes</a>', url, count)

    view_notes_link.short_description = "Notes" #change the colomn name


@admin.register(StudiesNotes)
class StudiesNotesAdmin(admin.ModelAdmin):
    autocomplete_fields = ("chapter",)
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

    @staticmethod
    def view_chapter_link(obj):
        url = (
            reverse("admin:studies_chapter_changelist")
            + "?"
            + urlencode({"id": f"{obj.chapter.id}"})
        )
        return format_html('<a href="{}"> link</a>', url)

    view_chapter_link.short_description = "chapter"


@admin.register(StudiesNotesProgression)
class StudiesNotesProgressionAdmin(admin.ModelAdmin):
    autocomplete_fields = ("notes",)
    actions = ['update_lvl_5', 'update_lvl_6', 'update_lvl_7', 'update_lvl_8']
    list_display = (
        "id",
        "user",
        "note_text",
        "is_recto",
        "notes",
        "level",
        "last_studied_date",
        "next_studied_date",
    )
    list_editable = ("level",)
    list_per_page = 200
    list_select_related = ['notes', 'user']
    search_fields = (
        "id", "user__email__istartswith"
    )
    list_filter = ("level",)

    @staticmethod
    def note_text(obj):
        return obj.notes.text_recto
    
    @admin.action(description="update lvl to 5")
    def update_lvl_5(self, request, queryset):
        queryset.update(level=5)
        self.message_user(request, "updated to lvl 5")
        
    @admin.action(description="update lvl to 6")
    def update_lvl_6(self, request, queryset):
        queryset.update(level=6)
        self.message_user(request, "updated to lvl 6")
        
    @admin.action(description="update lvl to 7")
    def update_lvl_7(self, request, queryset):
        queryset.update(level=7)
        self.message_user(request, "updated to lvl 7")
    
    @admin.action(description="update lvl to 8")
    def update_lvl_8(self, request, queryset):
        queryset.update(level=8)
        self.message_user(request, "updated to lvl 8")

@admin.register(GlobalDailyAnalysis)
class GlobalDailyAnalysisAdmin(admin.ModelAdmin):
    autocomplete_fields = ("user",)
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
    autocomplete_fields = ("user",)
    fields = []
    list_display = (
        "date",
        "user",
        "number_of_studies",
        "number_of_win",
        "number_of_lose",
    )
