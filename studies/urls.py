from django.urls import path
from . import views

app_name = "studies"

urlpatterns = [
    path("", views.personal_home_view, name="personal_home"),

    # get
    path("book/<int:book>", views.book_view_only, name="book_only"),
    path("book/<int:book>/<int:chapter>",
         views.book_view_chapter, name="book_chapter"),

    path("note/<int:chapter>", views.custom_note_view, name="specific_note"),

    path("note/<int:chapter>/<int:note>",
         views.custom_note_view, name="specific_note"),




    # delete
    path("delete/book/<int:book>", views.delete_book, name="delete_book"),
    path("delete/chapter/<int:chapter>",
         views.delete_chapter, name="delete_chapter"),
    path("delete/note/<int:note>", views.delete_note, name="delete_note"),
    path("feed_db", views.add_data_in_db, name="feed_db"),
]
